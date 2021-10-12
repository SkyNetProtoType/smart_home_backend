from samsungtv import SamsungTV
from decouple import config
import re


class TV:
    '''A class that allows you to controll your Samsung Smart TV'''
    IP_ADDRESS = config("TV_IP")

    def __init__(self):
        self.__tv = SamsungTV(self.IP_ADDRESS)
    
    def toggle_power(self):
        '''Turns on/off the TV'''
        try:
            self.__tv.power()
        except Exception:
            print("Unable to turn on tv")
    
    def increase_volume(self, amount=3):
        '''Increases the volume by the specified amount. By default, that amout is 3'''

        self.__tv.volume_up(amount)
    
    def decrease_volume(self, amount=3):
        '''Decreases the volume by the specified amount. By default, that amout is 3'''
        
        self.__tv.volume_down(amount)

    def open_source(self):
        '''Opens the TVs source to show different connected devices'''

        self.__tv.source()
    
    def go_back(self):
        '''Goes back to the previous screen'''
        
        self.__tv.back()


    def _get_tv_command(self, command):
        '''Uses the user command to return a tv command to be used to control the TV'''

        tv_operation = ""
        if re.search("power|turn", command):
            tv_operation = "power"
        elif "volume" in command:
            volume_count = re.findall("\d", command) # e.g. ['8']
            if "increase" in command:
                tv_operation = "increase " + volume_count[0]
            else:
                    tv_operation = "decrease " + volume_count[0]
        elif "back" in command:
            tv_operation = "back"
        elif "source" in command:
            tv_operation = "source"
        else:
            tv_operation = "unknown"
        
        return tv_operation


if __name__ == "__main__":
    pass
    # test_tv = TV()
    # test_tv.toggle_power()
    # test_tv.decrease_volume(5)
    # test_tv.open_source()
    # test_tv.go_back()
    
    # operation =  test_tv._get_tv_command("increase tv volume by 5")
    # print(operation)
    # operation =  test_tv._get_tv_command("decrease tv volume by 5")
    # print(operation)
    # operation =  test_tv._get_tv_command("turn on tv volume")
    # print(operation)
    # operation =  test_tv._get_tv_command("Open tv source")
    # print(operation)
    # operation =  test_tv._get_tv_command("Go back on tv")
    # print(operation)