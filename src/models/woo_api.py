import requests
import os
import json

auth_token = os.environ.get('WOOCOMMERCE_AUTH_TOKEN')
headers = {'Authorization': auth_token,
           'Content-type': 'application/json'}
mainUrl = 'https://anaramosmoda.com.br/wp-json/wc/v3/'


def wooRequests(type_of_req, urlEndPoint, queryParams, data):
    try:
        response = requests.request(
            type_of_req, mainUrl + urlEndPoint, headers=headers, params=queryParams, data=data)

    except:
        print("Resposta do Woocommerce - ", response)
        return 'Aconteceu um erro ao requisitar Woocommerce'

    else:
        print("Resposta do Woocommerce - ", response)
        print("Resposta do Woocommerce - ", response.text)

        return {
            "prod_info": response.json(),
            "status": response.status_code
        }


def getWooProcessingOrders():
    json_processing_orders = wooRequests(
        "GET", "orders/", {"status": "processing"}, None)
    return json_processing_orders


def getProductInfo(product_id):
    with open('src/db/products_info.json', 'r') as f:
        data = json.load(f)

    print("Buscando Informação sobre Produto no DB...")

    try:
        for product in data['products']:
            if product['id'] == product_id:
                print("Encontrado no DB")
                return product

    except KeyError:
        print('Ocorreu um problema no ID do produto')
        return None

    print("Buscando Informação sobre Produto no Woocommerce...")

    res = wooRequests('GET', f'products/{product_id}', None, None)

    if not res['status'] == 200:
        return None

    data['products'].append(res['prod_info'])

    with open('src/db/products_info.json', 'w') as f:
        json.dump(data, f, indent=2)

    print('Produto encontrado no Woocommerce e adicionado ao DB')
    return res['prod_info']
