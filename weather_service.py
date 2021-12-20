from decouple import config
import requests
from datetime import datetime
from pprint import pprint

API_KEY = config('WEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_ONE_CALL = "https://api.openweathermap.org/data/2.5/onecall"
WEATHER_ICON_LINK = " http://openweathermap.org/img/wn/10d@2x.png"
HTTP_OK = 200

def convert_to_fahrenheit(current_temp) -> int:
    return int((current_temp - 273.15) * 9/5 + 32)

def convert_to_localtime(epoch_timestamp, ignore_minutes=False):
    local_timestamp = datetime.fromtimestamp(epoch_timestamp)
    time_portion = datetime.strptime(local_timestamp.strftime("%m/%j/%y %H:%M"), "%m/%j/%y %H:%M").time()
    return time_portion.strftime("%I:%M").lstrip("0") if not ignore_minutes else time_portion.strftime("%I%p").lstrip("0")


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
    def get_current_report(state, city, zip) -> dict:
        '''
            Handles the request to get the current weather information. Makes
            a request to a third party service to get the data.
        '''

        url = f"{BASE_URL}?zip={zip}&appid={API_KEY}"
        response = requests.get(url)
        response_status_code = response.status_code

        if response_status_code != HTTP_OK:
            raise RuntimeError("Request Failed with a response status code: {}".format(response_status_code))

        data = response.json()
        main_info = data['main']
        temperature = convert_to_fahrenheit(main_info['temp'])
        feels_like = convert_to_fahrenheit(main_info['feels_like'])
        sunset_time = convert_to_localtime(data['sys']['sunset'])

        more_info = data['weather'][0]
        description = more_info['main'].lower()

        return {
            'temp': temperature,
            'feels_like': feels_like,
            'sunset': sunset_time,
            'sunset_unix': data['sys']['sunset'],
            'description': description,
            'state': state,
            'city' :city,
            'zipcode' : zip,
        }
    
    @staticmethod
    def get_hourly_info(lat, lon):
        '''Gets the hourly weather report and only keeps the next 3 hours'''

        result = []
        exclude = "minutely,daily"
        url = f"{BASE_URL_ONE_CALL}?lat={lat}&lon={lon}&exclude={exclude}&appid={API_KEY}"
        response = requests.get(url)
        status_code = response.status_code
        if status_code != HTTP_OK:
            raise RuntimeError("Request Failed with a response status code: {}".format(status_code))
        
        data = response.json()
        #current info
        current = data['current']
        result.append({
            "time": convert_to_localtime(current['dt'], ignore_minutes=True),
            "temp": convert_to_fahrenheit(current['temp']),
            "sunset": convert_to_localtime(current['sunset']),
            "feels_like": convert_to_fahrenheit(current['feels_like']),
            "description": current['weather'][0]['main'], 
            "chance_of_rain": "",
        })

        #hourly info
        hourly_info = data['hourly'][1:4] #next 3 hours after current hour
        alerts = []
        try:
            alerts = data['alerts']
        except KeyError:
            alerts = [{"event": "no alerts"}]
        for info in hourly_info:
            single_hour_info = {
                "time" : convert_to_localtime(info['dt'], ignore_minutes=True),
                "temp": convert_to_fahrenheit(info['temp']),
                "feels_like": convert_to_fahrenheit(info['feels_like']),
                "chance_of_rain":str(int(info['pop']) * 100), 
                "description": info['weather'][0]['main'].lower(),
                "sunset": ""
                }
            result.append(single_hour_info)
        return result



    


if __name__ == "__main__":
    # assert(WeatherService.validate_request_args("texas", "pflugerville", "7866") == False)
    # print(WeatherService.get_current_report("Texas","Pflugerville","78660"))
    pprint(WeatherService.get_hourly_info(lat=30.4421, lon=-97.6299))