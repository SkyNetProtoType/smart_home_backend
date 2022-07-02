
import unittest
import json
import mock
from weather_service import WeatherService

# Read about mocking here: https://www.toptal.com/python/an-introduction-to-mocking-in-python

class WeatherServiceTest(unittest.TestCase):
    '''Tests getting weather info'''
    TESTDATA = None

    @classmethod
    def setUpClass(cls):
        with open ('weather_payloads.json') as file:
          cls.TESTDATA = json.load(file)

    @mock.patch("weather_service.requests")
    def test_getHourlyInfo_for_only_current_hour_returns_current_hour_data(self, mock_reqs):
        pass

    def test_getHourlyInfo_for_next_3_hours_returns_3_hours_data(self):
        pass

    def test_getHourlyInfo_for_only_next_3_days_returns_next_3_days_data(self):
        pass
        

if __name__ == '__main__':
    unittest.main()