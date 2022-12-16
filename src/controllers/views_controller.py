from flask import render_template, make_response
from flask.wrappers import Response


def home():
    return make_response(render_template("home.html"), 200, )


def order_form():
    return make_response(render_template("order-form.html"))
