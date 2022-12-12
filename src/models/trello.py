from src.models.order import Order
from datetime import datetime
import requests
import json
import os


class Trello:
    cards_endpoint = 'https://api.trello.com/1/cards/'
    trelloKey = os.environ.get('TRELLO_KEY')
    trelloToken = os.environ.get('TRELLO_TOKEN')
    headers_request = {"Accept": "application/json"}

    def __init__(self, card_name, desc, list_id, labels_ids, attachs_urls):
        self.name = card_name
        self.labels_ids = labels_ids
        self.list_id = list_id
        self.desc = desc
        self.start = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.attachs_urls = attachs_urls

    def __repr__(self) -> str:
        return f'Nome do \nCartão: {self.name}'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def create_card(cls, name, list_id, desc, start, labels_ids):
        url = Trello.cards_endpoint
        query = {"name": name,
                 "labels_ids": labels_ids,
                 "idList": list_id,
                 "key": Trello.trelloKey,
                 "token": Trello.trelloToken,
                 "desc": desc,
                 "start": start
                 }

        response = requests.request(
            "POST", url, headers=Trello.headers_request, params=query)
        print('Trello - Criar cartão: ', response)

        return response.json()

    @classmethod
    def set_attachs(cls, card_id, attachs_urls):
        url = Trello.cards_endpoint + f"{card_id}/attachments"

        query = {
            'key': Trello.trelloKey,
            'token': Trello.trelloToken,
            'mimeType': 'image/jpg'
        }

        for attach_url in attachs_urls:
            query['url'] = attach_url

            response = requests.request(
                "POST", url, headers=Trello.headers_request, params=query)
            print('Resposta vindo Trello - Anexo ao Cartão: ', response)

    @classmethod
    def create_card_in_address_form_list(cls, user, order):
        card_desc = f'Nome : {user.name}\nRua/Avenida : {user.address_1}\nNúmero: {user.number}\nComplemento: {user.complement}\nBairro: {user.neighbor}\nObs: {user.observacao}\nCidade: {user.city}\nEstado: {user.state}\nCep: {user.cep}\n\n------------------------\n\nCPF: {user.cpf}\nNúmero WhatsApp: {user.zap}\nLink para o WhatsApp: \n{user.linkzap}'
        list_id = "6315059660711c0109c21c09"
        trello_card_labels = []
        start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        card_info = Trello.create_card(
            user.name, list_id, card_desc, start_time, trello_card_labels)

        urls_attachs_list = Order.get_products_imgs_urls_list(order.products)

        Trello.set_attachs(card_info['id'], urls_attachs_list)

        return card_info
