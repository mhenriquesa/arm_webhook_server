from flask import render_template, make_response
from src.models.order import OrderSite, OrderAddressForm, AdressFormLink
from src.utils.variables import ORDER_SAMPLE


def address_form(form_data):
    address_form = OrderAddressForm(form_data)
    address_form.create_trello_card()
    address_form.create_shipping_tag()
    return make_response(render_template("order-form_confirmation.html"), 200)


def new_order_site(order_info):
    if not order_info:
        order_info = ORDER_SAMPLE

    new_order = OrderSite(order_info)
    new_order.create_trello_card()
    new_order.create_shipping_tag()


def criar_link_form(link_data):
    address_form_link = AdressFormLink(link_data)
    address_form_link.create()
    return make_response(render_template("order-form-create-link_confirmation.html", link_form=address_form_link.link), 200)
