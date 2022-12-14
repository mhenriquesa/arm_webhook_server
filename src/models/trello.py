from datetime import datetime
import requests
import json
import os


class TrelloCard:
    cards_endpoint = 'https://api.trello.com/1/cards/'
    trelloKey = os.environ.get('TRELLO_KEY')
    trelloToken = os.environ.get('TRELLO_TOKEN')
    headers_request = {"Accept": "application/json"}

    def __init__(self, card_name, desc, list_id, labels_ids, attachs_urls):
        self.name = card_name
        self.labels_ids = labels_ids
        self.list_id = list_id
        self.desc = desc
        self.start = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.attachs_urls = attachs_urls

    def __repr__(self) -> str:
        return f'Nome do \nCartão: {self.name}'

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def create(self):
        url = TrelloCard.cards_endpoint
        query = {"name": self.name,
                 "labels_ids": self.labels_ids,
                 "idList": self.list_id,
                 "key": TrelloCard.trelloKey,
                 "token": TrelloCard.trelloToken,
                 "desc": self.desc,
                 "start": self.start
                 }

        response = requests.request(
            "POST", url, headers=TrelloCard.headers_request, params=query)
        print('TrelloCard - Criar cartão: ', response)

        return response.json()

    @classmethod
    def set_attachs(cls, card_id, attachs_urls):
        url = TrelloCard.cards_endpoint + f"{card_id}/attachments"

        query = {
            'key': TrelloCard.trelloKey,
            'token': TrelloCard.trelloToken,
            'mimeType': 'image/jpg'
        }

        for attach_url in attachs_urls:
            query['url'] = attach_url

            response = requests.request(
                "POST", url, headers=TrelloCard.headers_request, params=query)
            print('Resposta vindo TrelloCard - Anexo ao Cartão: ', response)

        return
