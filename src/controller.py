from src.trello_api import createCardOnTrelloList
# listId = '6302dd26f5539012a2430c4e' #Pedidos a Fazer - CRM e Pedidos
# labelsList = ['63037804ceeaa106a8d69189'] #Tag: Site

def createNewOrderRotine(order_informations):
  order_id = str(order_informations['id'])
  first_name = order_informations['billing']['first_name']
  last_name = order_informations['billing']['last_name']
  line_items = order_informations['line_items']
  order_products = []

  for product in line_items:
    prod_id = product['product_id']
    order_products.append(prod_id)

  card_name = f"# {order_id} - {first_name} {last_name} / {order_products} "
  listId = '631397afbd8be200c4e5b6e9' #Pedidos a Fazer - Teste em automação
  card_desc = ''
  labelsList = []

  createCardOnTrelloList(card_name, listId, card_desc, labelsList)