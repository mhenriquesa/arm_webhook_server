#cria as etiquetas de envio no melhor envio. (coloca no carrinho)
import os
import requests
token = os.environ.get('ARM_MENVIO')
main_url = "https://melhorenvio.com.br/api/v2/me/"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': token,
    'User-Agent': 'Aplicação henriqueator@gmail.com'
    }

def addShippigTagToCart(ship_info):
    response = requests.request("POST", main_url + "cart", headers=headers, data=ship_info)

    print('Status do Pedido : ')
    print(response.text)