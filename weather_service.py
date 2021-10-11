from decouple import config
import requests
from datetime import datetime

API_KEY = config('WEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
WEATHER_ICON_LINK = " http://openweathermap.org/img/wn/10d@2x.png"

def convert_to_fahrenheit(current_temp) -> int:
    return int((current_temp - 273.15) * 9/5 + 32)

def convert_to_localtime(epoch_timestamp):
    local_timestamp = datetime.fromtimestamp(epoch_timestamp)
    time_portion = datetime.strptime(local_timestamp.strftime("%m/%j/%y %H:%M"), "%m/%j/%y %H:%M").time()
    return time_portion.strftime("%I:%M %p")

class WeatherService:
    '''A class that accesses the weather report for a given city'''

    @staticmethod
    def validate_request_args(state, city, zipcode):
        '''Validates the weather query parameters in the url request'''
        if city == None or state == None or zipcode == None or len(zipcode) != 5:
            return False
        else:
            return True

    @staticmethod    
    def get_weather_report(state, city, zip) -> dict:
        '''
            Handles the request to get the current weather information. Makes
            a request to a third party service to get the data.
        '''

        url = f"{BASE_URL}zip={zip}&appid={API_KEY}"
        response = requests.get(url)
        response_status_code = response.status_code

        if response_status_code != 200:
            raise RuntimeError("Request Failed with a response status code: {}".format(response_status_code))

        data = response.json()
        main_info = data['main']
        temperature = convert_to_fahrenheit(main_info['temp'])
        min_temperature = convert_to_fahrenheit(main_info['temp_min'])
        max_temperature = convert_to_fahrenheit(main_info['temp_max'])
        sunset_time = convert_to_localtime(data['sys']['sunset'])

        more_info = data['weather'][0]
        weather_icon = WEATHER_ICON_LINK + more_info['icon']
        description = more_info['main'].lower()
        more_description = more_info['description']

        return {
            'temp': temperature,
            'min_temp': min_temperature,
            'max_temp': max_temperature,
            'sunset': sunset_time,
            'description': description,
            'more_description': more_description,
            'icon': weather_icon,
            'state': state,
            'city' :city,
            'zipcode' : zip,
        }


    


if __name__ == "__main__":
    assert(WeatherService.validate_request_args("texas", "pflugerville", "7866")
    == False)
    # WeatherService.get_weather_report("Texas", "Pflugerville", "78660")
    print(WeatherService.get_weather_report("Texas","Pflugerville","78660"))
