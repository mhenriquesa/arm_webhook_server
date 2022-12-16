import re

class Preference:
  def __init__(self, items, payer, back_urls, auto_return):
    self.items = items
    self.payer = payer
    self.back_urls = back_urls
    self.auto_return = auto_return

class New_Order:
  def __init__(self, order_informations):
    self.id = order_informations['id']
    self.client_first_name = order_informations['shipping']['first_name']
    self.client_name = self.client_first_name + ' ' + order_informations['shipping']['last_name']
    self.cpf = order_informations['billing']['cpf']
    self.address =order_informations['shipping']['address_1']
    self.number = order_informations['shipping']['number']
    self.complement = order_informations['shipping']['address_2']
    self.neighbor = order_informations['shipping']['neighborhood']
    self.city = order_informations['shipping']['city']
    self.state = order_informations['shipping']['state']
    self.cep = order_informations['shipping']['postcode']
    self.formattedPhone = order_informations['billing']['phone']
    self.phoneOnlyNumbers = re.sub(r'[^0-9]', '', self.formattedPhone)
    self.linkzap = f'https://api.whatsapp.com/send?phone=55{self.phoneOnlyNumbers}'
    self.pendingOrdersTrelloList = '63191b83a8e4af048326a8b2' #Pendentes de aprovação
    self.products = order_informations['line_items']
    self.card_desc = f'''Fone para contato: {self.formattedPhone}\nLink WhatsApp: \n{self.linkzap}'''


