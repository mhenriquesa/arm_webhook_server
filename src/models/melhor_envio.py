import os
import requests
import json


class MelhorEnvio:
    TOKEN = os.environ.get('ARM_MENVIO')
    EMAIL = os.environ.get('MENVIO_USER_EMAIL')
    main_url = "https://melhorenvio.com.br/api/v2/me/"

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': TOKEN,
        'User-Agent': f'Aplicação {EMAIL}'
    }

    @classmethod
    def send_request(cls, endpoint, payload, description_req):
        response = requests.request(
            "POST", MelhorEnvio.main_url + endpoint, headers=MelhorEnvio.headers, data=payload)

        print(
            f"Resposta do Melhor envio para requisição - {description_req}: ", response)
        print(response.text)

        return response.json()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class ShippingTag(MelhorEnvio):
    CPF_CIA = os.environ.get("CPF_CIA")
    ADDRESS_1_CIA = os.environ.get("ADDRESS_1_CIA")
    COMPLEMENT_CIA = os.environ.get("COMPLEMENT_CIA")
    CEP_CIA = os.environ.get("CEP_CIA")
    EMAIL_CIA = os.environ.get("EMAIL_CIA")

    def __init__(self, shipping_name, shipping_cpf, shipping_address_1, shipping_complement, shipping_number, shipping_bairro, shipping_city, shipping_state, shipping_cep, products, tags):
        self.service = 1
        self.agency = 1
        self.de = {
            "name": "Ana Ramos Moda",
            "phone": "",
            "email": ShippingTag.EMAIL_CIA,
            "document": ShippingTag.CPF_CIA,
            "company_document": "",
            "state_register": "",
            "address": ShippingTag.ADDRESS_1_CIA,
            "complement": ShippingTag.COMPLEMENT_CIA,
            "number": "599",
            "district": "Jardim do Estádio",
            "city": "Santo André",
            "country_id": "BR",
            "postal_code": ShippingTag.CEP_CIA,
            "note": ""
        }
        self.to = {
            "name": shipping_name,
            "phone": "",
            "email": "",
            "document": shipping_cpf,
            "company_document": "",
            "state_register": "",
            "address": shipping_address_1,
            "complement": shipping_complement,
            "number": shipping_number,
            "district": shipping_bairro,
            "city": shipping_city,
            "state_abbr": shipping_state,
            "country_id": "BR",
            "postal_code": shipping_cep,
            "note": ""
        }
        self.products = products
        self.volumes = [
            {
                "height": 10,
                "width": 5,
                "length": 10,
                "weight": 0.2
            }
        ]
        self.plataform = "Ana Ramos Moda - Moda Feminina"
        self.tags = tags

    def send_to_cart(self):
        payload = self.to_json().replace('"de":', '"from":')

        MelhorEnvio.send_request("cart", payload, "Criar etiqueta no carrinho")
