from os import abort
from flask import Flask, jsonify, request
from flask_cors import CORS
from weather import Weather
app = Flask(__name__)
# app.debug = True
CORS(app)


def is_valid_weather_args(city, state, zipcode):
  '''Validates the weather query parameters in the url request'''

  if city == None or state == None or zipcode == None:
    return False
  elif len(zipcode) != 5:
    return False
  else:
    return True

@app.route("/")
def test():
  '''Default mapping for testing the endpoint'''
  return jsonify({'welcome': 'Backend service works!'})


def get_weather():
  '''
    Retrieves the weather information using the weather API
    returns: a JSON with the weather information if all arguments are valid and
            the weather report is sucessfully retrieved, otherwise returns an empty
            JSON object.
  '''

  city = request.args.get('city')
  state = request.args.get('state')
  zipcode = request.args.get('zipcode')
  weather = Weather()
  if is_valid_weather_args(city, state, zipcode) and \
    weather.get_weather_report(city, state, zipcode):
      return jsonify(weather.get_json())
  else:
    return jsonify({})


if __name__ == "__main__":
  # assert is_valid_weather_args(None,None,None) == False # no valid arguments passed
  # assert is_valid_weather_args("homewood",None,None) == False # only one valid argument passed
  # assert is_valid_weather_args(None,"Illinois","78834") == False # only two valid arguments passed
  # assert is_valid_weather_args("homewood","Illinois","7834") == False # all valid except zipcode
  # assert is_valid_weather_args("homewood","Illinois","78834") == True # all valid arguments passed
  
  # print("All test passed!")

  app.run()
