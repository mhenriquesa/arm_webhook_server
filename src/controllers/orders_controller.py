from src.models.trello import TrelloCard
from src.models.user import User
from src.models.order import Order

def start_address_form_routine(data):
  user = User(data)
  order = Order(data)

  products_imgs_urls_list = order.get_products_imgs_urls_list()

  trello_card_desc = f'Nome : {user.name}\nRua/Avenida : {user.address_1}\nNúmero: {user.number}\nComplemento: {user.complement}\nBairro: {user.neighbor}\nObs: {user.observacao}\nCidade: {user.city}\nEstado: {user.state}\nCep: {user.cep}\n\n------------------------\n\nCPF: {user.cpf}\nNúmero WhatsApp: {user.zap}\nLink para o WhatsApp: \n{user.linkzap}'
  trello_list_id = "6315059660711c0109c21c09"
  trello_card_labels = []
  
  trello_card = TrelloCard(user.name, trello_card_desc, trello_list_id, trello_card_labels, products_imgs_urls_list )
  card_info = trello_card.create()

  trello_card.set_attachs(card_info['id'])
  