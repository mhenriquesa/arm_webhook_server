# Podemos obter informações de quadros, listas cartões do trello usando a API
import os
import requests
import json
from datetime import datetime

trelloKey = os.environ.get('TRELLO_KEY') 
trelloToken = os.environ.get('TRELLO_TOKEN')
mainTrelloEndpoint = 'https://api.trello.com/1/'
headers = {"Accept": "application/json"}

def getAttachmentsFromCard(idCard):
  url = mainTrelloEndpoint + f"cards/{idCard}/attachments"
  query = {
  'key': trelloKey,
  'token': trelloToken
  }

  response = requests.request("GET", url, headers=headers, params=query)

  listCards = response.json()
  return listCards

def getCardsFromATrelloList(listId):
  url = mainTrelloEndpoint + f"lists/{listId}/cards"
  query = {
   'key': trelloKey,
   'token': trelloToken
  }

  response = requests.request("GET", url, headers=headers, params=query)
  print(response)

  cardsList = response.json()

  return cardsList

def createAttachmentsOnCard(idCard, urlAttach):
    url = mainTrelloEndpoint + f"cards/{idCard}/attachments"
    query = {
        'key': trelloKey,
        'token': trelloToken,
        'url' : urlAttach,
        'mimeType' : 'image/jpg'
    }

    response = requests.request("POST", url, headers=headers, params=query)
    print(response.text)

def createCardOnATrelloList(card_name, listId, desc, idLabelsList, urlAttachs):
  
    url = mainTrelloEndpoint + "cards/"
    query = {"name" : card_name, 
    "idLabels" : idLabelsList, 
    "idList" : listId, 
    "key": trelloKey, 
    "token" : trelloToken, 
    "desc" : desc,
    "start" : datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') 
    }
    
    response = requests.request("POST", url, headers=headers, params=query)
    print(response.text)
    card_info = response.json()

    if urlAttachs: 
        for url in urlAttachs:
            createAttachmentsOnCard(card_info['id'], url)
