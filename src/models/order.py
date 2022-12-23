from src.models.melhor_envio import ShippingTag
from src.models.woo_api import getProductInfo
from src.models.trello import TrelloCard
from datetime import datetime
import json
import re


class Order:
    def __init__(self, client_first_name, client_last_name, cpf, client_address_1, number, complement, neighbor, city, state, cep, phone, shipping_type, shipping_price, products_info, total_value, forma_pgto, trello_list):
        self.client_first_name = client_first_name
        self.client_last_name = client_last_name
        self.cpf = cpf
        self.client_address_1 = client_address_1
        self.number = number
        self.complement = complement
        self.neighbor = neighbor
        self.city = city
        self.state = state
        self.cep = cep
        self.phone = phone
        self.shipping_type = shipping_type
        self.shipping_price = shipping_price
        self.products_info = products_info
        self.products_details = {
            "declaration_info": [],
            "imgs_urls_list": []
        }
        self.total_value = total_value
        self.forma_pgto = forma_pgto
        self.trello_list = trello_list

        phoneOnlyNumbers = re.sub(r'[^0-9]', '', self.phone)
        self.linkzap = f'https://api.whatsapp.com/send?phone=55{phoneOnlyNumbers}'
        self.date_start = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    def get_trello_card_desc(self):
        return f'Nome : {self.client_first_name} {self.client_last_name}\nRua/Avenida : {self.client_address_1}\nNúmero: {self.number}\nComplemento: {self.complement}\nBairro: {self.neighbor}\nCidade: {self.city}\nEstado: {self.state}\nCep: {self.cep}\n\n------------------------\n\nCPF: {self.cpf}\nLink para o WhatsApp: \n{self.linkzap}'

    def get_trello_card_name(self):
        return f"{self.client_first_name} {self.client_last_name}"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def create_trello_card(self):
        card_name = self.get_trello_card_name()
        desc = self.get_trello_card_desc()
        card_labels_ids = None
        list_id = self.trello_list

        trello_card = TrelloCard(
            card_name, desc, list_id, card_labels_ids, self.products_info)

        card_info = trello_card.create()
        return card_info

    def create_shipping_tag(self):
        shipping_tag = ShippingTag(f"{self.client_first_name} {self.client_last_name}", self.cpf, self.client_address_1, self.complement, self.number, self.neighbor,
                                   self.city, self.state, self.cep, self.products_details['declaration_info'], self.shipping_price, self.shipping_type, None)
        shipping_tag.send_to_cart()
        return


class OrderAddressForm(Order):
    def __init__(self, form_data):
        client_first_name = form_data['info']['name_1']
        client_last_name = form_data['info']['name_2']
        cpf = form_data['info']['cpf']
        client_address_1 = form_data['info']['address_1']
        number = form_data['info']['address_number']
        complement = form_data['info']['complemento']
        neighbor = form_data['info']['bairro']
        city = form_data['info']['cidade']
        state = form_data['info']['estado']
        cep = form_data['info']['cep']
        phone = form_data['info']['zap']
        shipping_type = form_data['tipo_frete']
        shipping_price = form_data['preco_frete']
        products_info = form_data['produtos']
        forma_pgto = form_data['forma_pgto']
        total_value = None
        trello_list = "6315059660711c0109c21c09"

        super().__init__(client_first_name, client_last_name, cpf,
                         client_address_1, number, complement, neighbor, city, state, cep, phone, shipping_type, shipping_price, products_info, total_value, forma_pgto, trello_list)
        self.id = None

    def turn_codes_str_into_int_list(self):
        products_codes_in_list = re.findall(r"\d{4}", self.products_info)
        return [int(i) for i in products_codes_in_list]

    def get_products_details(self):
        if self.products_info == None:
            print('Não há códigos de roupas para anexar ao cartão!')
            return None

        codes_int_list = self.turn_codes_str_into_int_list()

        for code in codes_int_list:
            prodinfo = getProductInfo(code)

            if prodinfo == None:
                return None

            imgs_src = prodinfo['images'][0]['src']
            product_name = prodinfo['name']
            product_price = prodinfo['price']

            info_for_declaration = {
                "name": product_name,
                "quantity": 1,
                "unitary_value": product_price
            }

            self.products_details['imgs_urls_list'].append(imgs_src)
            self.products_details['declaration_info'].append(
                info_for_declaration)

    def create_trello_card(self):
        card_info = super().create_trello_card()
        self.get_products_details()

        return TrelloCard.set_attachs(
            card_info['id'], self.products_details['imgs_urls_list'])


class OrderSite(Order):
    def __init__(self, order_data):
        client_first_name = order_data['shipping']['first_name']
        client_last_name = order_data['shipping']['last_name']
        cpf = order_data['billing']['cpf']
        client_address_1 = order_data['shipping']['address_1']
        number = order_data['shipping']['number']
        complement = order_data['shipping']['address_2']
        neighbor = order_data['shipping']['neighborhood']
        city = order_data['shipping']['city']
        state = order_data['shipping']['state']
        cep = order_data['shipping']['postcode']
        phone = order_data['billing']['phone']
        shipping_type = order_data['shipping_lines'][0]['method_id']
        shipping_price = order_data['shipping_lines'][0]['total']
        products_info = order_data['line_items']
        total_value = order_data['total']
        trello_list = '63191b83a8e4af048326a8b2'

        super().__init__(id, client_first_name, client_last_name, cpf,
                         client_address_1, number, complement, neighbor, city, state, cep, phone, shipping_type, shipping_price, products_info, total_value, trello_list)

        self.id = order_data['id']

    def get_products_details(self):
        if not self.products_info:
            print('Não há códigos de roupas para anexar ao cartão!')
            return None

        for product in self.products_info:
            img_url = product['image']['src']
            name = product['name']
            quantity = product['quantity']
            price = product['subtotal']

            info_for_declaration = {
                "name": name,
                "quantity": quantity,
                "unitary_value": price
            }

            self.products_details['imgs_urls_list'].append(img_url)
            self.products_details['declaration_info'].append(
                info_for_declaration)

            print(self.products_details)

    def create_trello_card(self):
        card_info = super().create_trello_card()
        self.get_products_details()

        TrelloCard.set_attachs(
            card_info['id'], self.products_details['imgs_urls_list'])
        return


class AdressFormLink():
    def __init__(self, link_data):
        self.cod_produtos = link_data['cod_produtos']
        self.preco_frete = link_data['preco_frete']
        self.tipo_frete = link_data['tipo_frete']
        self.forma_pgto = link_data['forma_pgto']
        self.link = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    def create(self):
        link = 'https://anaramosmoda.com/formulario-de-pedido?'

        if self.cod_produtos:
            link = f"{link}produtos={self.cod_produtos}&"

        if self.preco_frete:
            link = f"{link}preco_frete={self.preco_frete}&"

        self.link = link
