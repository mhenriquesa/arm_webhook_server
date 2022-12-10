from src.models.trello import Trello
from src.models.user import User
from src.models.order import Order

def start_address_form_routine(data):
  user = User(data)
  order = Order(data)

  Trello.create_card_in_address_form_list(user, order)
  