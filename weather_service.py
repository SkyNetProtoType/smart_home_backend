from decouple import config
import requests


API_KEY = config('WEATHER_API_KEY')
CITY = config('HOME_CITY')
STATE = config('HOME_STATE')
ZIP = config('HOME_ZIP')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
WEATHER_ICON_LINK = " http://openweathermap.org/img/wn/10d@2x.png"

class WeatherService:
    '''A class that accesses the weather report for a given city'''

    def __init__(self):
        pass

        
    def get_weather_report(self, city=CITY, state=STATE, zip=ZIP) -> dict:
        '''
            Handles the request to get the current weather information

            #Parameters:
                city: the city where you want the weather info
                state: the associated state of the city
                zipcode: the zip code of the city
            
            #Returns:
                JSON/Dict containing the weather information

            #Exceptions:
                Raises an exception if the response status is not OK (200)
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

        weather_report = {
            'temp': temperature,
            'description': description,
            'more_description': more_description,
            'icon': weather_icon,
            'state': state,
            'city' :city,
            'zipcode' : zip,
        }

        return weather_report


    


if __name__ == "__main__":
    weather_service = WeatherService()
    print(weather_service.get_weather_report("Pflugerville", "Texas", "78660"))
