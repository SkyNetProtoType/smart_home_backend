from os import stat
from decouple import config
import requests

API_KEY = config('WEATHER_API_KEY')
CITY = config('HOME_CITY')
STATE = config('HOME_STATE')
ZIP = config('HOME_ZIP')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
WEATHER_ICON_LINK = " http://openweathermap.org/img/wn/10d@2x.png"

class Weather:
    '''A class that accesses the weather report for a given city'''

    def __init__(self):
        self._temperature = 0
        self._json = {}
        self._zip = ZIP
        self._city = CITY
        self._state = STATE
        
    def get_weather_report(self, city=CITY, state=STATE, zip=ZIP) -> bool:
        '''Gets the current temperature and humidity for the given city'''

        url = f"{BASE_URL}zip={zip}&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            main_info = data['main']
            self._temperature = int((main_info['temp'] - 273.15) * 9/5 + 32)

            more_info = data['weather'][0]
            weather_icon = WEATHER_ICON_LINK + more_info['icon']
            description = more_info['main'].lower()
            more_description = more_info['description']

            self._json = {
                'temp': self._temperature,
                'description': description,
                'more_description': more_description,
                'icon': weather_icon,
                'state': state,
                'city' :city,
                'zipcode' : zip,
            }
            return True
        
        return False

    def get_json(self):
        return self._json

    def get_temperature(self):
        '''Returns the current temperature in degrees Fahrenheit'''
        return self._temperature
    
    def get_city(self):
        '''Returns the current city for which the weather is being reported'''
        return self._city

    def get_state(self):
        '''Returns the current state for which the weather is being reported'''
        return self._state
    


if __name__ == "__main__":
    weather = Weather()
    is_report_successful = weather.get_weather_report() 
    if not is_report_successful:
        print ("Unable to retrieve weather info for", CITY)
    else:
        print(f"{CITY:-^30}")
        print(weather.get_json())
        # print(f"Temperature: {weather.get_temperature()}")
    


#    print(f"Weather Report: {report[0]['description']}")