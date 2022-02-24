from time import sleep
from yeelight import Bulb, BulbException
from decouple import config
from enum import Enum

LIVING_ROOM_FLOOR_LAMP = config("FLOOR_LAMP_BULB")

class LightType(Enum):
    LIVING_ROOM_FLOOR_LAMP = 1


class LightService:
    # floor_lamp.start_music()
    # print("came to static field first")

    def __init__(self) -> None:
        print ("came to constructor")

    @staticmethod
    def turn_on(light_type: object):
        status = "already_on"
        floor_lamp = Bulb(LIVING_ROOM_FLOOR_LAMP)   # create a new socket connection to the bulb
        lamp_properties = floor_lamp.get_properties()
        is_already_on = lamp_properties['power'] == 'on'
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP and not is_already_on:
            for attempt in range(1, 4): #3 times
                try:
                    floor_lamp.turn_on()
                    status = "successful"
                except BulbException as e:
                    print (f'Attempt {attempt}: {e}')
                    status = "error"
                except Exception as e:
                    print (f'Attempt {attempt}: {e}')
                    status = "error"
                else:
                    break #exit attempting once succeeded.
        return status
    
    @staticmethod
    def turn_off(light_type: object):
        status = "already off"
        floor_lamp = Bulb(LIVING_ROOM_FLOOR_LAMP)   # create a new socket connection to the bulb
        lamp_properties = floor_lamp.get_properties()
        is_already_off = lamp_properties['power'] == 'off'
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP and not is_already_off:
            for attempt in range(3):
                try:
                    floor_lamp.turn_off()
                    status = "succesful"
                except BulbException as e:
                    print (f'Attempt {attempt}: {e}')
                    status = "error"
                except Exception as e:
                    print (f'Attempt {attempt}: {e}')
                    status = "error"
                else:
                    break #exit attempting once succeeded.
        return status

    @staticmethod
    def toggle(light_type: object):
        status = ""
        floor_lamp = Bulb(LIVING_ROOM_FLOOR_LAMP)   # create a new socket connection to the bulb
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP:
            try:
                status = floor_lamp.toggle()
            except BulbException as e:
                print (e)
                status = "error"
        return status
    
    @staticmethod
    def adjust_brightness(light_type: object, amount: int):
        status = ""
        floor_lamp = Bulb(LIVING_ROOM_FLOOR_LAMP)   # create a new socket connection to the bulb
        lamp_properties = floor_lamp.get_properties()
        is_already_off = lamp_properties['power'] == 'off'
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP and not is_already_off:
            for attempt in range(3):
                try:
                    status = floor_lamp.set_brightness(amount)
                except BulbException as e:
                    print (f'Attempt {attempt}: {e}')
                    status = "error"
                except Exception as e:
                    print (f'Attempt {attempt}: {e}')
                    status = "error"
                else:
                    break # exit attempt loop
        return status


if __name__ == "__main__":
    LightService()
    # print(LightService.lamp_properties)
    LightService.turn_on(LightType.LIVING_ROOM_FLOOR_LAMP)
    sleep(5)
    LightService.turn_off(LightType.LIVING_ROOM_FLOOR_LAMP)

         


 
