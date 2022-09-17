from src.melhor_envio_api import addShippigTagToCart
from src.trello_api import getCardsFromATrelloList
from src.trello_api import createCardOnATrelloList
from src.trello_api import getAttachmentsFromCard
from src.woo_api import createPendingOrder
from src.woo_api import getProductInfo
import requests
import json
import re


# listId = '6302dd26f5539012a2430c4e' #Pedidos a Fazer - CRM e Pedidos
# labelsList = ['63037804ceeaa106a8d69189'] #Tag: Site

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

def productExistsInStock(product_id):
    with open('src/stock.json') as f:
        stock = json.load(f)
    f.close

    return True if str(product_id) in stock else False

def productExistsInShopList(product_id):
    with open('src/shop_list.json') as f:
        shop_list = json.load(f)
    f.close

    for product in shop_list['products']:
        product_in_shop_list_id = product['product_id']
        if product_in_shop_list_id == product_id:
            print('Foi encontrado um produto na lista')
            return True
    
    print('NÃO Foi encontrado um produto na lista de Compra')
    return False
    
def addProductToShopList(name, product_id,  imgUrl):
    product_to_add = {
        "product_id" : product_id,
        "fornecedor" : '',
        "quantity" : 1,
        "img" : imgUrl['src'],
        "name" : name
    }

    with open('src/shop_list.json') as f:
        json_shop_list = json.load(f)
    f.close()

    json_shop_list['products'].append(product_to_add)

    with open('src/shop_list.json', 'w') as f:
        json.dump(json_shop_list, f)

def increaseProductQuantityOnShopList(productID, howMany):
    with open('src/shop_list.json') as f:
        json_shop_list = json.load(f)
    f.close
    
    for product in json_shop_list['products']:
        if productID == product['product_id']:
            product['quantity'] += howMany

            with open('src/shop_list.json', 'w') as f:
               json.dump(json_shop_list, f)
            f.close

            return
    print('Não existe esse produto na lista. Algo errado')

def insertOrderProductsOnShopList(order_informations):
    order_products = order_informations['line_items']

    for product in order_products:
        new_order_product_id = product['product_id'] #int

        if productExistsInStock(new_order_product_id):
            print(f'''{product['name']} já tem em estoque.''')
            print('Não adicionado à lista de compra.')
            print('Checkando próximo produto...')
            continue

        print('Produto não existe em estoque...')

        if productExistsInShopList(new_order_product_id):
            print(f'''{product['name']} já está na lista de compra''')

            increaseProductQuantityOnShopList(new_order_product_id, product['quantity'])
            print('Foi aumentado a quatidade de um produto da lista')
            continue
        
        print('Produto não está na lista de compras')
        addProductToShopList(product['name'], product['product_id'],  product['image'])

        print('Foi adicionado um produto à lista de compras')

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
    email = data['fields[email][value]']
    forma = data['fields[forma][value]']

    produtos = data['fields[produtos][value]']
    products_codes = re.findall(r"\d{4}", produtos)
    products_codes_int = [int(i) for i in products_codes]
    line_items = []

    print(products_codes_int)


    # for code in products_codes_int:
    #     product_info = getProductInfo(code)
    #     prod_dict = {
	# 		"id": product_info['id'],
	# 		"name": product_info['name'],
	# 		"price": product_info['sale_price'],
	# 		"image": product_info['images'][0]['src'],
	# 		"quantity": 1
	# 		}
        
    #     line_items.append(prod_dict)
    #     print(json.dumps(product_info, indent=3))




    phoneOnlyNumbers = re.sub(r'[^0-9]', '', zap)
    linkzap = f'https://api.whatsapp.com/send?phone=55{phoneOnlyNumbers}'

    card_desc = { 
        f'Nome : {name}\nRua/Avenida : {address_1}\nNúmero: {number}\nComplemento: {complement}\nBairro: {neighbor}\nObs: {observacao}\nCidade: {city}\nEstado: {state}\nCep: {cep}\n\n------------------------\n\nCPF: {cpf}\nNúmero WhatsApp: {zap}\nLink para o WhatsApp: \n{linkzap}'
    }

    createCardOnATrelloList(name, trelloList, card_desc, [], None)
    createNewOrderShippingTagOnCart(name, cpf, address_1, number, complement, neighbor, city, state, cep, None )
    # createPendingOrder(name, '', address_1, number, neighbor, complement, city, state, cep, email, zap, line_items, cpf, forma)


    

def insertOrderOnWhatsOrdersList():
    pass

def posVendaFormRoutine(data):
    trello_list = '631916f1d6c70804cdf94931'
    motivo = data['Qual o motivo do seu contato?']
    buyer = data['Nome do Comprador']
    pedido = data['Número do Pedido ARM']
    date = data['Date']
    zap = data['WhatsApp para Contato']
    acontecido = data['O que aconteceu? Como posso ajudar?']
    imgs = data['Clique aqui para enviar algumas fotos para ajudar na avaliação']

    card_desc = ''

    createCardOnATrelloList(buyer, trello_list, card_desc, [], imgs)

def sendMsgToCustomer(clientFirstName, phone ,order_id):
    phoneOnlyNumbers = re.sub(r'[^0-9]', '', phone)
    zapnumber = '55' + str(phoneOnlyNumbers) + "@c.us"

    msg = f'Olá, {clientFirstName}! Tudo bem?\n\nSou a Aninha da Ana Ramos Moda\n\nParabéns por sua compra. Assim que eu tiver o seu código de rastreamento, venho aqui te informar.\n\n Agora é só aguardar seu look em casa! \n\nNúmero do pedido: {order_id}'
    url = 'https://arm-whatsapp.herokuapp.com/customer_update'
    body = {
        "number" : zapnumber,
        "message" : msg
    }

    response = requests.request("POST", url, data=body)
    print(response.text)


    
def sendOrderToWhatsAppList(client_name, products_images):
    # url = 'http://localhost:8000/add_order_to_Whatsapp_list'
    url = 'https://arm-whatsapp.herokuapp.com/add_order_to_Whatsapp_list'
    body = {
        "chatId" : '120363043296540441@g.us',
        "client_name" : client_name,
        "products_images" : products_images,
    }

    response = requests.request("POST", url, data=body)
    print(response.text)
        

def newOrderRoutine(order_informations):
    order = order_informations['id']
    client_first_name = order_informations['shipping']['first_name']
    client_name = client_first_name + ' ' + order_informations['shipping']['last_name']
    cpf = order_informations['billing']['cpf']
    address =order_informations['shipping']['address_1']
    number = order_informations['shipping']['number']
    complement = order_informations['shipping']['address_2']
    neighbor = order_informations['shipping']['neighborhood']
    city = order_informations['shipping']['city']
    state = order_informations['shipping']['state']
    cep = order_informations['shipping']['postcode']
    formattedPhone = order_informations['billing']['phone']
    phoneOnlyNumbers = re.sub(r'[^0-9]', '', formattedPhone)
    linkzap = f'https://api.whatsapp.com/send?phone=55{phoneOnlyNumbers}'
    pendingOrdersTrelloList = '63191b83a8e4af048326a8b2' #Pendentes de aprovação

    products = order_informations['line_items']
    urlsImagesProducts = []
    products_codes = ''

    for product in products:
        if product['variation_id'] > 0:
            products_codes = f"{products_codes} {str(product['variation_id'])}"
        else:
            products_codes = f"{products_codes} {str(product['product_id'])}"
      
        prod_img_url = product['image']['src']
        urlsImagesProducts.append(prod_img_url)
    
    card_desc = f'''Fone para contato: {formattedPhone}\nLink WhatsApp: \n{linkzap}'''

        
    createNewOrderShippingTagOnCart(client_name, cpf, address, number, complement, neighbor, city, state, cep, products)
    createCardOnATrelloList(f"#{order} - {client_name} / {products_codes}",pendingOrdersTrelloList, card_desc, [], urlsImagesProducts)
    sendOrderToWhatsAppList(client_name, urlsImagesProducts)
    sendMsgToCustomer(client_first_name, formattedPhone, order)
    
def getWhatsAppOrdersList(trelloOrdersCards):
    whatsAppOrders = []

    for card in trelloOrdersCards[9:]:
        cardAttachsList = getAttachmentsFromCard(card['id'])
        urlsImagesAttachs = []

        for attach in cardAttachsList:
            urlImgAttach = attach['previews'][2]['url']

            urlsImagesAttachs.append(urlImgAttach)

        whatsAppOrder = {"name" : card['name'], "products" : urlsImagesAttachs}
        # print(whatsAppOrder)

        whatsAppOrders.append(whatsAppOrder)

    return whatsAppOrders

def sendOrdersListToWhatsApp(whatsAppOrders):
    url = 'http://localhost:8000/whatsAppApi'
    headers = {'Content-Type': 'application/json'}

    body = {
        "chatId" : '120363043296540441@g.us', #Grupo Alvo
        "ordersList" : whatsAppOrders
    }
    try:

        response = requests.request("POST", url, data=json.dumps(body), headers=headers)
        print(response.text)
    except requests.exceptions.ConnectionError:

        print('Ocorreu um erro na tentativa de conexão com WhatsApp API')
        
def newWhatsAppOrdersListRoutine():
    trelloOrdersList = '6302dd26f5539012a2430c4e'
    trelloOrdersCards = getCardsFromATrelloList(trelloOrdersList)
    whatsAppOrders = getWhatsAppOrdersList(trelloOrdersCards)
    print(whatsAppOrders)
    sendOrdersListToWhatsApp(whatsAppOrders)








    