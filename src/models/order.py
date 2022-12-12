from src.woo_api import getProductInfo
from datetime import datetime
import re
import json


class Order:
    def __init__(self, form_data) -> None:
        products_codes_from_url = form_data['fields[produtos][value]']

        self.id = ''  # get_order_id
        self.buyer_id = ''  # get_user_id
        self.products = Order.get_products_from_code_str(
            products_codes_from_url)
        self.shipping_type = 'PAC'
        self.shipping_price = 0
        self.date_purchase = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.total_value = ''

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def get_products_imgs_urls_list(cls, products_list):
        products_imgs_urls_list = []

        for product in products_list:
            products_imgs_urls_list.append(product['img_url'])

        return products_imgs_urls_list

    @classmethod
    def get_products_from_code_str(cls, code_in_str):
        order_products_list = []

        products_codes_in_list = re.findall(r"\d{4}", code_in_str)
        products_codes_numbers = [int(i) for i in products_codes_in_list]

        for code in products_codes_numbers:
            product_info = getProductInfo(code)

            order_products_list.append(
                {
                    "id": product_info['id'],
                    "name": product_info['name'],
                    "price": product_info['price'],
                    "img_url": product_info['images'][0]['src']
                }
            )

        return order_products_list
