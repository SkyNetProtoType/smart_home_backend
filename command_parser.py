from weather import Weather
from arithmetic import BasicMath
from tv_controller import TV
from encyclopedia import Encyclopedia
import re

class Command_Parser:
    '''This class takes parses a command from the user and determines which
    response to return to the AI assistant
    '''

    def __init__(self) -> None:
        self._command = None
        self._math = BasicMath()
        self._weather = Weather()
  
    
    def get_reponse(self, user_command):
        '''
            Takes in a user command and determines which response function to return to the AI.
            The AI doesn't know which specific method is being called. The order of if
            statements matter because of how questions can be asked
            Uses the Factory Design Pattern
        '''
        self._command = user_command.lower() # if the command is to be used anywhere else

        if "weather" in user_command or "temperature" in user_command:
            return self.__report_weather
        elif re.search("[+-/*//]", user_command):
            return self.__solve_arithmetic
        elif re.search("^what is", user_command):
            return self.__search_encyclopedia
        elif "tv" in user_command or "television" in user_command:
            return self.__control_tv
        else:
            return self.__unknown_response

    def __search_encyclopedia(self):
        enc = Encyclopedia()
        summary = ""
        search_results = enc.search(self._command)
        if len(search_results) != 0:
            summary = enc.summarize(search_results[0])
        else:
            summary = "Sorry. No results were found for your question"
        return summary


    def __control_tv(self):
        '''Uses the tv command to determine what TV operation to perform'''

        tv = TV()
        tv_command = tv._get_tv_command(self._command)
        if tv_command == "power":
            tv.toggle_power()
        elif tv_command == "back":
            tv.go_back()
        elif tv_command == "source":
            tv.open_source()
        elif tv_command== "unknown":
            return "Unknown TV command"
        else:
            # then it has to be about the volume
            split_command = tv_command.split()
            volume_type = split_command[0]
            if volume_type == "increase":
                tv.increase_volume(split_command[1])
            else: 
                tv.decrease_volume(split_command[1])
        
        return "Done!"

    def __solve_arithmetic(self):
        result = self._math.solve(self._command)
        return f"The result is {result}"


    def __report_weather(self):
        '''Returns the weather report of the current city'''

        city = self._weather.get_city()
        state = self._weather.get_state()
        is_report_successful = self._weather.get_weather_report() 

        if not is_report_successful:
            return f"Unable to retrieve weather information for {city}, {state}"
        else:
            temp = self._weather.get_temperature()
            return f"The current temperature in {city}, {state} is {temp} degrees fahrenheit"
    
    def __unknown_response(self):
        return "I am not sure how to answer this yet"

    def set_command(self, test_command):
        self._command = test_command

if __name__ == "__main__":
    parser = Command_Parser()
    response = parser.get_reponse("What is the temperature right now")
    print(response())
    response =  parser.get_reponse("What is the 2 * 5")
    print(response())
    response =  parser.get_reponse("What is differentiation")
    print(response())
    