from src.controller import createNewOrderShippingTagOnCart
from src.controller import insertOrderProductsOnShopList
from src.controller import addressFormRoutine
from src.controller import createNewOrderCard
from flask import request, Response, Blueprint
import json

main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    return "Hello world!"

@main.route('/woo_webhook/new_order', methods=['POST'])
def newOrderRotine():  
    order_informations = request.get_json(silent=True, force=True)

    with open('new_order.json', 'w') as f:
        json.dump(order_informations, f)

    if not order_informations :
        order_informations = {'id': 5212, 'parent_id': 0, 'status': 'processing', 'currency': 'BRL', 'version': '6.8.2', 'prices_include_tax': False, 'date_created': '2022-09-03T17:43:34', 'date_modified': '2022-09-03T17:43:38', 'discount_total': '0.00', 'discount_tax': '0.00', 'shipping_total': '0.00', 'shipping_tax': '0.00', 'cart_tax': '0.00', 'total': '2.00', 'total_tax': '0.00', 'customer_id': 1, 'order_key': 'wc_order_NV5eR8sqabW2k', 'billing': {'first_name': 'Moisés Henrique', 'last_name': 'Silva Araujo', 'company': '', 'address_1': 'Rua Adriático', 'address_2': 'Bloco c Ap 23', 'city': 'Santo André', 'state': 'SP', 'postcode': '09172-180', 'country': 'BR', 'email': 'henriqueator@gmail.com', 'phone': '(11) 98294-2057', 'number': '599', 'neighborhood': 'Jardim do Estádio', 'persontype': 'F', 'cpf': '00753216450', 'rg': '', 'cnpj': '', 'ie': '', 'birthdate': '', 'sex': '', 'cellphone': ''}, 'shipping': {'first_name': 'Moisés Henrique', 'last_name': 'Silva Araujo', 'company': '', 'address_1': 'Rua Sao Vicente', 'address_2': '', 'city': 'Natal', 'state': 'RN', 'postcode': '59037-660', 'country': 'BR', 'phone': '', 'number': '599',
        'neighborhood': 'Alecrim'}, 'payment_method': 'cod', 'payment_method_title': 'Pagamento na entrega', 'transaction_id': '', 'customer_ip_address': '2804:54:14fe:2f00:1c2:cd10:4984:787e', 'customer_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', 'created_via': 'checkout', 'customer_note': '', 'date_completed': None, 'date_paid': None, 'cart_hash': '49d60906bd651045cc4927d67d7d3265', 'number': '3898', 'meta_data': [{'id': 47683, 'key': '_billing_cpf', 'value': '007.532.164-50'}, {'id': 47684, 'key': '_billing_number', 'value': '599'}, {'id': 47685, 'key': '_billing_neighborhood', 'value': 'Jardim do Estádio'}, {'id': 47686, 'key': '_shipping_number', 'value': '599'}, {'id': 47687, 'key': '_shipping_neighborhood', 'value': 'Jardim do Estádio'}, {'id': 47688,
        'key': 'is_vat_exempt', 'value': 'no'}, {'id': 47689, 'key': '_wcf_flow_id', 'value': '847'}, {'id': 47690, 'key': '_wcf_checkout_id', 'value': '849'}, {'id': 47691, 'key': '_wc_facebook_for_woocommerce_order_placed', 'value': 'yes'}, {'id': 47694, 'key': 'melhorenvio_quotation_v2', 'value': {'2': {'id': 2, 'name': 'SEDEX', 'price': '10.31', 'custom_price': '10.31', 'discount': '10.69', 'currency': 'R$', 'delivery_time': 4, 'delivery_range': {'min': 3, 'max': 4}, 'custom_delivery_time': 4, 'custom_delivery_range': {'min': 3, 'max': 4}, 'packages': [{'price': '10.31', 'discount': '10.69', 'format': 'box', 'weight': '0.20', 'insurance_value': '0.00', 'products': [{'id': '3885', 'quantity': 1}], 'dimensions': {'height': 5, 'width': 11, 'length': 16}}],
        'additional_services': {'receipt': False, 'own_hand': False, 'collect': False}, 'company': {'id': 1, 'name': 'Correios', 'picture': 'https://www.melhorenvio.com.br/images/shipping-companies/correios.png'}}, '3': {'id': 3, 'name': '.Package', 'price': '16.55', 'custom_price': '16.55',
        'discount': '6.30', 'currency': 'R$', 'delivery_time': 6, 'delivery_range': {'min': 5, 'max': 6}, 'custom_delivery_time': 6, 'custom_delivery_range': {'min': 5, 'max': 6}, 'packages': [{'format': 'box', 'weight': '0.20', 'insurance_value': '2.00', 'products': [{'id': '3885', 'quantity': 1}], 'dimensions': {'height': 5, 'width': 10, 'length': 10}}], 'additional_services': {'receipt': False, 'own_hand': False, 'collect': False}, 'company': {'id': 2, 'name': 'Jadlog', 'picture': 'https://www.melhorenvio.com.br/images/shipping-companies/jadlog.png'}}, '4': {'id': 4, 'name': '.Com', 'price': '14.00', 'custom_price': '14.00', 'discount': '0.98', 'currency': 'R$', 'delivery_time': 5, 'delivery_range': {'min': 4, 'max': 5}, 'custom_delivery_time': 5, 'custom_delivery_range': {'min': 4, 'max': 5}, 'packages': [{'format': 'box', 'weight': '0.20', 'insurance_value': '2.00', 'products': [{'id': '3885', 'quantity': 1}], 'dimensions': {'height': 5, 'width': 10, 'length': 10}}], 'additional_services': {'receipt': False, 'own_hand': False, 'collect': False}, 'company': {'id': 2, 'name': 'Jadlog', 'picture': 'https://www.melhorenvio.com.br/images/shipping-companies/jadlog.png'}}, '9': {'id': 9, 'name': 'Rodoviário', 'price': '161.73', 'custom_price': '161.73', 'discount': '0.00', 'currency': 'R$', 'delivery_time': 6, 'delivery_range': {'min': 6, 'max': 6}, 'custom_delivery_time': 6, 'custom_delivery_range': {'min': 6,
        'max': 6}, 'packages': [{'format': 'box', 'weight': '0.20', 'insurance_value': '2.00', 'products': [{'id': '3885', 'quantity': 1}], 'dimensions': {'height': 5, 'width': 10, 'length': 10}}],
        'additional_services': {'receipt': False, 'own_hand': False, 'collect': True}, 'company': {'id': 5, 'name': 'Via Brasil', 'picture': 'https://www.melhorenvio.com.br/images/shipping-companies/viabrasil.png'}}, '22': {'id': 22, 'name': 'Rodoviário', 'price': '23.07', 'custom_price': '23.07', 'discount': '17.52', 'currency': 'R$', 'delivery_time': 2, 'delivery_range': {'min': 1, 'max': 2}, 'custom_delivery_time': 2, 'custom_delivery_range': {'min': 1, 'max': 2}, 'packages': [{'format': 'box', 'weight': '0.20', 'insurance_value': '2.00', 'products': [{'id': '3885', 'quantity': 1}], 'dimensions': {'height': 5, 'width': 10, 'length': 10}}], 'additional_services': {'receipt': False, 'own_hand': False, 'collect': False}, 'company': {'id': 12, 'name': 'Buslog', 'picture': 'https://www.melhorenvio.com.br/images/shipping-companies/buslog.png'}}, 'date_quotation': '2022-09-03 20:43:03', 'choose_method': 2, 'free_shipping': False, 'diff': True}}, {'id': 47700, 'key': '_new_order_email_sent', 'value': 'true'}, {'id': 47701, 'key': '_wc_facebook_for_woocommerce_purchase_tracked', 'value': 'yes'}], 'line_items': [{'id': 449, 'name': 'Produto teste', 'product_id': 3999, 'variation_id': 0, 'quantity': 1, 'tax_class': '', 'subtotal': '2.00', 'subtotal_tax': '0.00', 'total': '2.00', 'total_tax': '0.00', 'taxes': [], 'meta_data': [], 'sku': '', 'price': 2, 'image': {'id': '', 'src': 'http://anaramosmoda.com.br/wp-content/uploads/2022/09/wp-1662398190618.jpg'}, 'parent_name': None},{'id': 449, 'name': 'Produto teste', 'product_id': 3885, 'variation_id': 0, 'quantity': 1, 'tax_class': '', 'subtotal':
        '2.00', 'subtotal_tax': '0.00', 'total': '2.00', 'total_tax': '0.00', 'taxes': [], 'meta_data': [], 'sku': '', 'price': 2, 'image': {'id': '', 'src': 'http://anaramosmoda.com.br/wp-content/uploads/2022/09/wp-1662398178249.jpg'}, 'parent_name': None}], 'tax_lines': [], 'shipping_lines': [{'id': 450, 'method_title': 'Frete grátis', 'method_id': 'free_shipping', 'instance_id': '29', 'total': '0.00', 'total_tax': '0.00', 'taxes': [], 'meta_data': [{'id': 3601, 'key': 'Itens', 'value': 'Produto teste &times; 1', 'display_key': 'Itens', 'display_value': 'Produto teste &times; 1'}]}], 'fee_lines': [], 'coupon_lines': [], 'refunds': [], 'payment_url': 'https://anaramosmoda.com.br/finalizar-compra/order-pay/3898/?pay_for_order=true&key=wc_order_NV5eR8sqabW2k', 'is_editable': False, 'needs_payment': False, 'needs_processing': True,
        'date_created_gmt': '2022-09-03T20:43:34', 'date_modified_gmt': '2022-09-03T20:43:38', 'date_completed_gmt': None, 'date_paid_gmt': None, 'correios_tracking_code': '', 'currency_symbol': 'R$', '_links': {'self': [{'href': 'https://anaramosmoda.com.br/wp-json/wc/v3/orders/3898'}], 'collection': [{'href': 'https://anaramosmoda.com.br/wp-json/wc/v3/orders'}], 'customer': [{'href': 'https://anaramosmoda.com.br/wp-json/wc/v3/customers/1'}]}}

    createNewOrderCard(order_informations)
    createNewOrderShippingTagOnCart(order_informations)
    insertOrderProductsOnShopList(order_informations)
    
    return Response(status=200)

@main.route('/mp_webhook', methods=['POST'])
def mpWebhook():
    #recebe o payload enviado pelo request recebido
    data = request.get_json(silent=True, force=True)
    print(data)

    if data is not None:
      return Response(status=200)
    return Response(status=200)

@main.route('/address-form', methods=['POST'])
def recevied_address_form():
    data = request.form.to_dict()

    addressFormRoutine(data)
    
    if data:
        return Response(status=200)

    return Response(status=500)
