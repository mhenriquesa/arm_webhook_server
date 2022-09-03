from flask import request, Response, Blueprint
from src.trello_api import createCardOnTrelloList

main = Blueprint('main', __name__)


@main.route('/')
def hello_world():
    return "Hello world!"

@main.route('/woo_webhook/new_order', methods=['POST'])
def wooWebhook():
    # listId = '6302dd26f5539012a2430c4e' #Pedidos a Fazer - CRM e Pedidos
    listId = '631397afbd8be200c4e5b6e9' #Pedidos a Fazer - Teste em automação
    card_desc = 'Teste'
    card_name = '# - Nome da cliente - Telefone'
    # labelsList = ['63037804ceeaa106a8d69189'] #Tag: Site
    labelsList = [] 

    data = request.get_json(silent=True, force=True)
    #recebe o payload enviado pelo request recebido
    # print(data)
    # order_id = 'S' + str(data['id'])
    # order_client_name = data['billing']['first_name'] + ' ' + data['billing']['last_name']
    # order_product_id = data['line_items']['product_id'] if data['line_items']['variation_id'] == 0 else data['line_items']['variation_id']
    # phone = data['billing']['phone']

    # createCardOnTrelloList(f'{order_id} {order_client_name} {phone}', '6302dd26f5539012a2430c4e', 'Teste')
    createCardOnTrelloList(card_name, listId, card_desc, labelsList)

    if data is not None:
      #Responde o status OK 200
      return Response(status=200)
    return Response(status=200)

@main.route('/mp_webhook', methods=['POST'])
def mpWebhook():
    #recebe o payload enviado pelo request recebido
    data = request.get_json(silent=True, force=True)
    print(data)

    if data is not None:
      #Responde o status OK 200
      return Response(status=200)
    return Response(status=200)