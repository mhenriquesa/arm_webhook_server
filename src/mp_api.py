import requests

def createPreferenceMp():
  url = "https://api.mercadopago.com/checkout/preferences"
  headers = {}
  query = {}

  response = requests.request("GET", url, headers=headers, params=query)
  print(response)

  cardsList = response.json()

  return cardsList