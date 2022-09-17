import requests
import os
import json

auth_token = os.environ.get('WOOCOMMERCE_AUTH_TOKEN')
headers = {'Authorization': 'Bearer ' + auth_token, 'Content-type' : 'application/json'}
mainUrl = 'https://anaramosmoda.com.br/wp-json/wc/v3/'

def wooRequests(type_of_req, urlEndPoint, queryParams, data):
	response = requests.request(type_of_req, mainUrl + urlEndPoint, headers=headers, params=queryParams, data=data)
	json_response = response.json()
	
	print(json.dumps(json_response, indent=4))
	return json_response


#Retorna um json com os pedidos em status 'Processing'
def getWooProcessingOrders():
	json_processing_orders = wooRequests("GET", "orders/", {"status" : "processing"}, None)
	# processing_orders = json.dumps(json_processing_orders, indent=3)
	return json_processing_orders

def getProductInfo(id):
	product_info = wooRequests('GET', f'products/{id}', None, None) 
	print(product_info)
	return product_info


def createPendingOrder(first_name, last_name, address, number, neighbor, complement, city, state, postcode, email, phone, products, cpf, forma ):
	order_sample = {
		"payment_method": "bacs",
		"payment_method_title": "Solicitou pagamento via PIX" if forma == "pix" else "Solicitou pagamento via Link do Mercado Pago",
		"set_paid": False,
		"billing": {
			"first_name": first_name,
			"last_name": last_name,
			"address_1": address,
			"address_2": complement,
			"city": city,
			"state": state,
			"postcode": postcode,
			"country": "BR",
			"email": email,
			"phone": phone,
		},
		"shipping": {
			"first_name": first_name,
			"last_name": last_name,
			"address_1": address,
			"address_2": complement,
			"city": city,
			"state": state,
			"postcode": postcode,
			"country": "BR"
		},
		"meta_data" : [
			{
				"id" : 45294, 
				"key" : '_billing_cpf', 
				"value" : cpf
			},
			{
				"id" : 45295, 
				"key" : '_billing_number', 
				"value" : number
			},
			{
				"id" : 45296, 
				"key" : '_billing_neighborhood', 
				"value" : neighbor
			},
			{
				"id" : 45297, 
				"key" : '_shipping_number',
				"value" : number
			},
			{
				"id" : 45298, 
				"key" : '_shipping_neighborhood',
				"value" : neighbor
			},
		],
		"line_items": [{"product_id": product['id'],"quantity": 1} for product in products],
		"shipping_lines": [{ 
				"method_id": "free_shipping",
				"method_title": "Frete Grátis",
				"total": "0"
			}] 
	}

	pendingOrder = json.dumps(order_sample)

	pendingOrderInformations = wooRequests('POST', 'orders', None, pendingOrder )
	print(json.dumps(pendingOrderInformations, indent=3))
	return 
