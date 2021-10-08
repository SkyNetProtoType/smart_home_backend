from decouple import config
import requests

API_KEY = config('WEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
WEATHER_ICON_LINK = " http://openweathermap.org/img/wn/10d@2x.png"

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
        temperature = int((main_info['temp'] - 273.15) * 9/5 + 32) # to Fahrenheit

        more_info = data['weather'][0]
        weather_icon = WEATHER_ICON_LINK + more_info['icon']
        description = more_info['main'].lower()
        more_description = more_info['description']

        return {
            'temp': temperature,
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
    # print(WeatherService.get_weather_report("Texas","Pflugerville","78660"))
