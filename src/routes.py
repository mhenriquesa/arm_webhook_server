from flask import request, Response, Blueprint
from src.controller import createNewOrderCard, createNewOrderShippingTagOnCart

main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    return "Hello world!"

@main.route('/woo_webhook/new_order', methods=['POST'])
def newOrderRotine():
    order_informations = request.get_json(silent=True, force=True)

    createNewOrderCard(order_informations)
    createNewOrderShippingTagOnCart(order_informations)
    # insertOrderProductsOnShopList(order_informations)
    
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