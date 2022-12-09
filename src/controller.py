from src.melhor_envio_api import addShippigTagToCart
# from src.trello_api import createCardOnATrelloList
from src.Models import New_Order
import json
import re

def createNewOrderShippingTagOnCart(client_name, cpf, address, number, complement, neighbor, city, state, cep, products):
    payload_sample = {
        "service": 2,
        "agency": 1,
        "from": {
            "name": "Ana Ramos Moda",
            "phone": "11982942057",
            "email": "sac@anaramosmoda.com.br",
            "document": "38477757828",
            "company_document": "",
            "state_register": "",
            "address": "Rua Adrático",
            "complement": "Bl C Ap 23",
            "number": "599",
            "district": "Santo André",
            "city": "São Paulo",
            "country_id": "BR",
            "postal_code": "09172180",
            "note": ""
        },
        "to": {
            "name": "Nome do destinatário",
            "phone": "",
            "email": "",
            "document": "25404918047",
            "company_document": "",
            "state_register": "",
            "address": "Endereço do destinatário",
            "complement": "Complemento",
            "number": "2",
            "district": "Bairro",
            "city": "Porto Alegre",
            "state_abbr": "RS",
            "country_id": "BR",
            "postal_code": "90570020",
            "note": ""
        },
        "products": [],
        "volumes": [
            {
            "height": 10,
            "width": 5,
            "length": 10,
            "weight": 0.2
            }
        ],
        "options": {
            "insurance_value": False,
            "receipt": False,
            "own_hand": False,
            "reverse": False,
            "non_commercial": False,
            "invoice": {
            "key": ""
            },
            "platform": "Ana Ramos Moda",
            "tags": [
            {
                "tag": "",
                "url": None
            }
            ]
        }
        }

    payload_sample["service"] = 2 if state == 'SP' else 1
    payload_sample["to"]['name'] = client_name
    payload_sample["to"]['address'] = address
    payload_sample["to"]['number'] = number
    payload_sample["to"]['complement'] = complement
    payload_sample["to"]['district'] = neighbor
    payload_sample["to"]['city'] = city
    payload_sample["to"]['state_abbr'] = state
    payload_sample["to"]['postal_code'] = cep
    payload_sample["products"] = products
   
    payload_sample["to"]['document'] = cpf
    

    products_declaration = []

    if products:

        for product in products:
            orderItems = { 
            "name" : product['name'],
            "quantity" : product['quantity'],
            "unitary_value" : product['price'],
            }

            products_declaration.append(orderItems)
        
    
    new_payload_json_string = json.dumps(payload_sample)

    addShippigTagToCart(new_payload_json_string)

def addressFormRoutine(data):
    #dados recebidos do formlário de endereço do site ARM
    trelloList = "6315059660711c0109c21c09" # Lista de destino no trello: Leads que preencheram Formulário

    # form_name = data['form[name]']
    name = data['fields[name][value]']
    address_1 = data['fields[address_1][value]']
    number = data['fields[number][value]']
    complement = data['fields[address_2][value]']
    neighbor = data['fields[neibor][value]']
    observacao = data['fields[observ][raw_value]'],
    city = data['fields[city][value]']
    state = data['fields[state][value]']
    cep = data['fields[cep][value]']
    cpf = data['fields[cpf][value]']
    zap = data['fields[zap][value]']

    produtos = data['fields[produtos][value]']
    products_codes = re.findall(r"\d{4}", produtos)
    products_codes_int = [int(i) for i in products_codes]

    print(products_codes_int)

    phoneOnlyNumbers = re.sub(r'[^0-9]', '', zap)
    linkzap = f'https://api.whatsapp.com/send?phone=55{phoneOnlyNumbers}'

    card_desc = { 
        f'Nome : {name}\nRua/Avenida : {address_1}\nNúmero: {number}\nComplemento: {complement}\nBairro: {neighbor}\nObs: {observacao}\nCidade: {city}\nEstado: {state}\nCep: {cep}\n\n------------------------\n\nCPF: {cpf}\nNúmero WhatsApp: {zap}\nLink para o WhatsApp: \n{linkzap}'
    }

    createNewOrderShippingTagOnCart(name, cpf, address_1, number, complement, neighbor, city, state, cep, None )
    # createCardOnATrelloList(name, trelloList, card_desc, [], None)

def getProductsInfoFromNewOrder(order_products):
    imgs_urls = []
    products_codes = ''

    for product in order_products:
        if product['variation_id'] > 0:
            products_codes = f"{products_codes} {str(product['variation_id'])}"
        else:
            products_codes = f"{products_codes} {str(product['product_id'])}"
      
        prod_img_url = product['image']['src']
        imgs_urls.append(prod_img_url)

    return {
        "imgs_urls" : imgs_urls,
        "codes" : products_codes
    }


def newOrderRoutine(order_informations):
    order = New_Order(order_informations)
    products_info = getProductsInfoFromNewOrder(order.products)
    
    createNewOrderShippingTagOnCart(order.client_name, order.cpf, order.address, order.number, order.complement, order.neighbor, order.city, order.state, order.cep, order.products)
    # createCardOnATrelloList(f"#{order} - {client_name} / {products_codes}",pendingOrdersTrelloList, card_desc, [], urlsImagesProducts)






    