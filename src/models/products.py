
class Product:
  def __init__(self, product_data) -> None:
    self.id = product_data['id']
    self.img_url = product_data['img_url']
    self.price = product_data['price']
    self.name = product_data['name']
    self.suplier = product_data['suplier']