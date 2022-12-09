import re
import json

class User:
  def __init__(self, form_data) -> None:
    self.id = ''
    self.name = form_data['fields[name][value]']
    self.address_1 = form_data['fields[address_1][value]']
    self.number = form_data['fields[number][value]']
    self.complement = form_data['fields[address_2][value]']
    self.neighbor = form_data['fields[neibor][value]']
    self.observacao = form_data['fields[observ][raw_value]']
    self.city = form_data['fields[city][value]']
    self.state = form_data['fields[state][value]']
    self.cep = form_data['fields[cep][value]']
    self.cpf = form_data['fields[cpf][value]']
    self.zap = form_data['fields[zap][value]']
    
    phoneOnlyNumbers = re.sub(r'[^0-9]', '', self.zap)
    self.linkzap = f'https://api.whatsapp.com/send?phone=55{phoneOnlyNumbers}'

  def to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__, indent=4)