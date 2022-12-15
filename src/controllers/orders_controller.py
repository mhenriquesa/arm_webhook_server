from src.models.order import OrderSite, OrderAddressForm
from src.utils.variables import ORDER_SAMPLE


def address_form(form_data):
    address_form = OrderAddressForm(form_data)
    address_form.create_trello_card()
    address_form.create_shipping_tag()


def new_order_site(order_info):
    if not order_info:
        order_info = ORDER_SAMPLE

    new_order = OrderSite(order_info)
    new_order.create_trello_card()
    # new_order.create_shipping_tag()
