from flask import Flask, json, jsonify, request
from flask_cors import CORS
from product_service import ProductService
from weather_service import WeatherService
from todoist_service import TodoistService

app = Flask(__name__)
# app.debug = True
CORS(app)


@app.route("/")
def test():
  return jsonify({'message': 'Backend service works!'})


@app.route("/weather/<state>/<city>/<zip>", methods=['GET'])
def weather(state, city, zip):
  if WeatherService.validate_request_args(state, city, zip) == False:
    raise RuntimeError(f"Invalid request args: {state}, {city}, {zip}")
  return jsonify(WeatherService.get_weather_report(state, city, zip))


@app.route("/products", methods = ['POST', 'GET'])
def products():
  if 'GET' == request.method:
    return jsonify(products = ProductService.get_products())
  else:
    product = request.get_json()
    product['addedToCart'] = 1 if product['addedToCart'] == True else 0
    ProductService.update_product(product)
    return jsonify(product['id'])


@app.route("/product", methods=['POST'])
def product():
  product = request.get_json()
  ProductService.add_new_product(product)
  print("New item inserted with id: ", product['id'])
  return jsonify(product['id'])


@app.route("/send/cart", methods=['POST'])
def send_cart_to_phone():
  cart_products = ProductService.get_cart_products()
  shopping_list_id = 2276166027
  service = TodoistService()
  for item in cart_products:
    service.addItemToProject(item['name'], shopping_list_id)
  


if __name__ == "__main__":
  app.run()
