from src.models.trello import TrelloCard
from src.models.user import User
from src.models.order import Order

def start_address_form_routine(form_data):
  user = User(form_data)
  order = Order(form_data)
  
  trello_card = TrelloCard(user, order)
  print(trello_card.to_json())
  