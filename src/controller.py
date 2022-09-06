from src.melhor_envio_api import addShippigTagToCart
from src.trello_api import createCardOnATrelloList
import json
import re

# listId = '6302dd26f5539012a2430c4e' #Pedidos a Fazer - CRM e Pedidos
# labelsList = ['63037804ceeaa106a8d69189'] #Tag: Site

def createNewOrderCard(order_informations):
    first_name = order_informations['billing']['first_name']
    formattedPhone = order_informations['billing']['phone']
    last_name = order_informations['billing']['last_name']
    cep = order_informations['billing']['postcode']
    line_items = order_informations['line_items']
    order_id = str(order_informations['id'])
    urlAttachs = []

    
    phoneOnlyNumbers = re.sub(r'[^0-9]', '', formattedPhone)
    linkzap = f'https://api.whatsapp.com/send?phone=55{phoneOnlyNumbers}'
    
    for product in line_items:
        prod_img_url = product['image']['src']
        urlAttachs.append(prod_img_url)
        
    card_desc = f'''Fone para contato: {formattedPhone}\nLink WhatsApp: \n{linkzap}'''            
    card_name = f"#{order_id} - {first_name} {last_name}"
    listId = '631397afbd8be200c4e5b6e9'
    labelsList = []

    createCardOnATrelloList(card_name, listId, card_desc, labelsList, urlAttachs)

def createNewOrderShippingTagOnCart(order_informations):
    ship_info = {
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
        "products": [
            {
            "name": "Papel adesivo para etiquetas 1",
            "quantity": 3,
            "unitary_value": 100
            },
            {
            "name": "Papel adesivo para etiquetas 2",
            "quantity": 1,
            "unitary_value": 700
            }
        ],
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
    if order_informations['shipping']['state'] == 'SP':
        ship_info["service"] = 2
    else:
        ship_info["service"] = 1

    client_name = ship_info["to"]['name'] = order_informations['shipping']['first_name'] + ' ' + order_informations['shipping']['last_name']
    cpf = ship_info["to"]['document'] = order_informations['billing']['cpf']
    ship_info["to"]['address'] = order_informations['shipping']['address_1']
    ship_info["to"]['complement'] = order_informations['shipping']['address_2']
    ship_info["to"]['number'] = order_informations['shipping']['number']
    ship_info["to"]['district'] = order_informations['shipping']['neighborhood']
    ship_info["to"]['city'] = order_informations['shipping']['city']
    ship_info["to"]['state_abbr'] = order_informations['shipping']['state']
    ship_info["to"]['postal_code'] = order_informations['shipping']['postcode']
    ship_info["products"] = []

    print('Nome da cliente :' + client_name)
    print('CPF :' + cpf)

    for product in order_informations['line_items']:
        orderItems = { 
        "name" : product['name'],
        "quantity" : product['quantity'],
        "unitary_value" : product['price'],
        }
        ship_info["products"].append(orderItems)
    
    
    ship_info_updated = json.dumps(ship_info)

    addShippigTagToCart(ship_info_updated)

def insertOrderProductsOnShopList():
    pass

def insertOrderOnWhatsOrdersList():
    pass
      