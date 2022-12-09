from src.models.trello import TrelloCard
from src.models.user import User
from src.models.order import Order

def start_address_form_routine(data):
  user = User(data)
  order = Order(data)
  print(order)
  print('==================')
  
  # trello_card = TrelloCard(user, order)

  