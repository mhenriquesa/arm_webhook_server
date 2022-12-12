from src.models.melhor_envio import ShippingTag
from src.models.trello import Trello
from src.models.order import Order
from src.models.user import User


def get_order_data(data):
    return Order(data)


def address_form(form_data):
    user = User(form_data)
    order = Order(form_data)

    Trello.create_card_in_address_form_list(user, order)

    new_tag = ShippingTag(user.name, user.cpf, user.address_1, user.complement, user.number, user.neighbor,
                          user.city, user.state, user.cep, order.products, order.shipping_price, order.shipping_type, None)
    new_tag.send_to_cart()


def create_card_in_address_form_list(user_data_from_form, order_data_from_form):
    Trello.create_card_in_address_form_list(
        user_data_from_form, order_data_from_form)


def create_shipping_tag_on_cart(user_data_from_form, order_data_from_form):

    new_tag = ShippingTag(user_data_from_form.name, user_data_from_form.cpf, user_data_from_form.address_1, user_data_from_form.complement, user_data_from_form.number, user_data_from_form.neighbor,
                          user_data_from_form.city, user_data_from_form.state, user_data_from_form.cep, order_data_from_form.products, order_data_from_form.shipping_price, order_data_from_form.shipping_type, None)
    new_tag.send_to_cart()
