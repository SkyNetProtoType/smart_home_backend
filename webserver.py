from typing import List
from flask import Flask, json, jsonify, request
from flask_cors import CORS
from product_service import ProductService
from weather_service import WeatherService
from todoist_service import TodoistService
from energy_service import handle_energy_data_request
from system_util import SystemUtil
from light_service import LightService, LightType
from settings_service import SettingsService
from pprint import pprint
import asyncio

app = Flask(__name__)
loop = asyncio.get_event_loop()
# app.debug = True
CORS(app)


@app.route("/")
def test():
  return jsonify({'message': 'Backend service works!'})


@app.route("/weather/<state>/<city>/<zip>", methods=['GET'])
def weather(state, city, zip):
  if WeatherService.validate_request_args(state, city, zip) == False:
    raise RuntimeError(f"Invalid request args: {state}, {city}, {zip}")
  return jsonify(WeatherService.get_current_report(state, city, zip))


@app.route("/weather/hourly", methods=['GET'])
def weather_hourly():
  return jsonify(hourly_weather_infos = WeatherService.get_hourly_info(lat=30.4421, lon=-97.6299))


@app.route("/products/<product_type>", methods = ['GET'])
def products(product_type):
  return jsonify(products = ProductService.get_products())


@app.route("/product/<action>/<product_type>", methods=['POST'])
def product(action, product_type):
  product = request.get_json()
  if action == "insert":
    ProductService.add_new_product(product)
    print("New item inserted with id: ", product['id'])

  elif action == 'update':
    product['addedToCart'] = 1 if product['addedToCart'] == True else 0
    ProductService.update_product(product)
  return jsonify(product['id'])


@app.route("/product/update/bulk", methods=["POST"])
def bulkProductUpdate() :
  products: List[dict] = request.get_json()
  for product in products:
    ProductService.update_product(product)
  return jsonify("All updated")


@app.route("/send/cart", methods=['POST'])
def send_cart_to_phone():
  cart_items = request.get_json()
  print(cart_items)
  cart_items = [item['name'] for item in cart_items]
  # pprint(cart_items)
  service = TodoistService()
  service.addItemsToProject(cart_items, project_id=2276166027)
  return jsonify(response = "success")


@app.route("/cart/queue", methods=['GET'])
def cart_queue():
  service = TodoistService()
  cart_queue_items = service.processQueueItems(queue_id=2285886894)
  return jsonify(cart_queue_items = cart_queue_items)
  
  
@app.route("/energy", methods=['GET'])
def energy():
  return jsonify(handle_energy_data_request())


@app.route("/battery", methods=['GET'])
def battery():
  return jsonify(SystemUtil.get_battery_info())


@app.route("/light/<light_type>/<action>/<value>", methods=['GET'])
def lights(light_type, action, value):
  if "living_floor_lamp" == light_type.lower() and "toggle" == action:
    if "on" == value:
      return jsonify(status = LightService.turn_on(LightType.LIVING_ROOM_FLOOR_LAMP))
    else:
      return jsonify(status = LightService.turn_off(LightType.LIVING_ROOM_FLOOR_LAMP))
    
   
  elif "living_floor_lamp" == light_type.lower() and "brightness" == action:
    return jsonify(status = LightService.adjust_brightness(LightType.LIVING_ROOM_FLOOR_LAMP, int(value)))

  else:
    return jsonify({"error": f"No light of type <{light_type}> has been setup"})


@app.route("/settings", methods=['POST','GET'])
def settings():
  if 'GET' == request.method:
    return jsonify(SettingsService.get_dashboard_settings())
  else:
    updated_settings = request.get_json()
    SettingsService.update_dashboard_settings(updated_settings)
    return jsonify({"status": "Update Successful"})

@app.route("/smart_plug/<toggle_state>", methods=["GET", "POST"])
def smart_plug(toggle_state: str):
  return jsonify({"plug_state": loop.run_until_complete(SystemUtil.toggle_smart_plug(toggle_state))})


if __name__ == "__main__":
  app.run()
