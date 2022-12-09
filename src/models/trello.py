from datetime import datetime
import requests
import json
import os

class TrelloCard:
  cards_endpoint = 'https://api.trello.com/1/cards/'
  trelloKey = os.environ.get('TRELLO_KEY') 
  trelloToken = os.environ.get('TRELLO_TOKEN')
  list_id = "6315059660711c0109c21c09"
  headers_request = {"Accept": "application/json"}
  
  def __init__(self, user):
    self.name = user.name
    self.labels_ids = None
    self.list_id = TrelloCard.list_id
    self.desc = f'Nome : {user.name}\nRua/Avenida : {user.address_1}\nNúmero: {user.number}\nComplemento: {user.complement}\nBairro: {user.neighbor}\nObs: {user.observacao}\nCidade: {user.city}\nEstado: {user.state}\nCep: {user.cep}\n\n------------------------\n\nCPF: {user.cpf}\nNúmero WhatsApp: {user.zap}\nLink para o WhatsApp: \n{user.linkzap}'
    self.start = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    self.urlsAttachs = None
  
  def __repr__(self) -> str:
    return f'Nome do \nCartão: {self.name}'


  def to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__, indent=4)
  
  def create(self):
    url = TrelloCard.cards_endpoint
    query = {"name" : self.name, 
    "labels_ids" : self.labels_ids, 
    "list_id" : self.list_id, 
    "key": TrelloCard.trelloKey, 
    "token" : TrelloCard.trelloToken, 
    "desc" : self.desc,
    "start" : self.start 
    }

    response = requests.request("POST", url, headers=TrelloCard.headers_request, params=query)
    print(response.json)
  
  def set_attachs(self, card_id):
    url = TrelloCard.cards_endpoint + f"{card_id}/attachments"
