from datetime import datetime
import json
import os

class TrelloCard:
  mainTrelloEndpoint = 'https://api.trello.com/1/'
  trelloKey = os.environ.get('TRELLO_KEY') 
  trelloToken = os.environ.get('TRELLO_TOKEN')
  list_id = "6315059660711c0109c21c09"
  
  def __init__(self, user, order):
    self.name = user.name
    self.idLabels = None
    self.idList = TrelloCard.list_id
    self.desc = f'Nome : {user.name}\nRua/Avenida : {user.address_1}\nNúmero: {user.number}\nComplemento: {user.complement}\nBairro: {user.neighbor}\nObs: {user.observacao}\nCidade: {user.city}\nEstado: {user.state}\nCep: {user.cep}\n\n------------------------\n\nCPF: {user.cpf}\nNúmero WhatsApp: {user.zap}\nLink para o WhatsApp: \n{user.linkzap}'
    self.start = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    self.urlsAttachs = None
  
  def __repr__(self) -> str:
    return f'Nome do \nCartão: {self.name}'


  def to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__, indent=4)
