from flask import request, Response, Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def hello_world():
    return "Hello world!"

@main.route('/woo_webhook', methods=['POST'])
def botwebhook():
    #recebe o payload enviado pelo request recebido
    data = request.get_json(silent=True, force=True)
    print(data)

    if data is not None:
      #Responde o status OK 200
      return Response(status=200)
    return Response(status=200)


@main.route('/mercadopago_webhook', methods=['POST'])
def mercadopagowebhook():
    data = request.get_json(silent=True, force=True)
    print(data)
    if data is not None:
        return Response(status=200)
    return Response(status=200)
