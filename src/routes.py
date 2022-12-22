from flask import request, Blueprint
from flask.wrappers import Response
from src.controllers import views_controller
from src.controllers import orders_controller

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def show_home():
    return views_controller.home()


@main.route('/formulario-de-pedido', methods=['GET'])
def order_form_page():
    return views_controller.order_form()


@main.route('/address-form', methods=['POST'])
def address_form():
    data = {
        "forma_pgto": request.form.get('forma_pgto'),
        "produtos": request.form.get('produtos'),
        "tipo_frete": request.form.get('tipo_frete'),
        "preco_frete": request.form.get('preco_frete'),
        "info": request.form.to_dict()
    }

    return orders_controller.address_form(data)


@main.route('/new_order', methods=['POST'])
def new_order_site():
    order_info = request.get_json(silent=True, force=True)
    orders_controller.new_order_site(order_info)

    return Response(status=201)
