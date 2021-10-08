
class Weather:
    '''A class that represents the weather report'''

    def __init__(self, report={}):
        self._report = report
        
    def get_report(self):
        '''Retrieves the current weather report'''
        return self._report
    
    def set_report(self, report):
        '''Sets the current weather report'''
        self._report = report

    def get_temperature(self):
        '''Returns the current temperature in degrees Fahrenheit'''
        return self._report['temp']
    
    def get_city(self):
        '''Returns the current city for which the weather is being reported'''
        return self._report['city']

    def get_state(self):
        '''Returns the current state for which the weather is being reported'''
        return self._report['state']
    


if __name__ == "__main__":
    from weather_service import WeatherService

    report = {}
    service = WeatherService()
    try:
        report = service.get_weather_report("Pflugerville", "Texas", "78660")
        weather = Weather(report)
        print(f"The weather for {weather.get_city()} is {weather.get_temperature()} degrees")
    except RuntimeError as re:
        print("Getting weather report was unsuccessful:", re)

    
    


#    print(f"Weather Report: {report[0]['description']}")