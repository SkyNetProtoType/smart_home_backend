from flask import Flask, jsonify, request
from flask_cors import CORS
from product_service import ProductService
from weather_service import WeatherService
import message_service

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


@app.route("/send/cart", methods=['POST'])
def send_cart_message():
  cart_products = ProductService.get_cart_products()
  cart_product_as_str = ProductService.convert_product_to_str(cart_products)
  sid = message_service.sendMessage(cart_product_as_str)
  print(f"Message sent: {sid} ")
  


if __name__ == "__main__":
  app.run()
