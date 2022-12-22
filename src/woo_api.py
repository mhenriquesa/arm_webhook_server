import requests
import os
import json

auth_token = os.environ.get('WOOCOMMERCE_AUTH_TOKEN')
print(auth_token)
headers = {'Authorization': auth_token,
           'Content-type': 'application/json'}
mainUrl = 'https://anaramosmoda.com.br/wp-json/wc/v3/'


def wooRequests(type_of_req, urlEndPoint, queryParams, data):
    response = requests.request(
        type_of_req, mainUrl + urlEndPoint, headers=headers, params=queryParams, data=data)
    json_response = response.json()

    print("Resposta do Woocommerce - ", response)
    print("Resposta do Woocommerce - ", response.text)

    return json_response


# Retorna um json com os pedidos em status 'Processing'
def getWooProcessingOrders():
    json_processing_orders = wooRequests(
        "GET", "orders/", {"status": "processing"}, None)
    # processing_orders = json.dumps(json_processing_orders, indent=3)
    return json_processing_orders


def getProductInfo(product_id):
    with open('src/db/products_info.json', 'r') as f:
        data = json.load(f)

    print("Buscando Informação sobre Produto no DB...")
    for product in data['products']:
        if product['id'] == product_id:
            print("Encontrado no DB")
            return product

    print("Buscando Informação sobre Produto no Woocommerce...")
    prod_info = wooRequests('GET', f'products/{product_id}', None, None)

    data['products'].append(prod_info)

    with open('src/db/products_info.json', 'w') as f:
        json.dump(data, f, indent=2)

    print('Produto encontrado no Woocommerce e adicionado ao DB')
    return prod_info
