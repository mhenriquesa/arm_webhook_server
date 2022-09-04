# Podemos obter informações de quadros, listas cartões do trello usando a API
import os
import requests

trelloKey = os.environ.get('TRELLO_KEY') 
trelloToken = os.environ.get('TRELLO_TOKEN')
mainTrelloEndpoint = 'https://api.trello.com/1/'


def getCardsFromATrelloList(listId):
  url = mainTrelloEndpoint + f"lists/{listId}/cards"
  headers = {"Accept": "application/json"}
  query = {
   'key': trelloKey,
   'token': trelloToken
  }

  response = requests.request("GET", url, headers=headers, params=query)
  print(response)

  listCards = response.json()

  return listCards



def createCardOnATrelloList(card_name, listId, desc, idLabelsList):
  url = mainTrelloEndpoint + "cards/"
  headers = {"Accept": "application/json"}
  query = {"name" : card_name, "idLabels" : idLabelsList, "idList" : listId, "key": trelloKey, "token" : trelloToken, "desc" : desc}
  
  response = requests.request("POST", url, headers=headers, params=query)
  print(response.text)