from flask import Flask, jsonify, request
from flask_cors import CORS
from weather import Weather
app = Flask(__name__)
app.debug = True
CORS(app)

@app.route("/")
def hello():
  return jsonify({'welcome': 'hello world'})

@app.route("/weather")
def get_weather():
  



if __name__ == "__main__":
  app.run()
