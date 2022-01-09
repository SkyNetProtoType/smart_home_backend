from yeelight import Bulb
from decouple import config
from enum import Enum

LIVING_ROOM_FLOOR_LAMP = config("FLOOR_LAMP_BULB")

class LightType(Enum):
    LIVING_ROOM_FLOOR_LAMP = 1


class LightService:
    floor_lamp = Bulb(LIVING_ROOM_FLOOR_LAMP)
    

    @staticmethod
    def turn_on(light_type: object):
        status = "already_on"
        lamp_properties = LightService.floor_lamp.get_properties()
        is_already_on = lamp_properties['power'] == 'on'
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP and not is_already_on:
            try:
                LightService.floor_lamp.turn_on()
                status = "successful"
            except Exception as e:
                print (e)
                status = "error"
        return status
    
    @staticmethod
    def turn_off(light_type: object):
        status = "already off"
        lamp_properties = LightService.floor_lamp.get_properties()
        is_already_off = lamp_properties['power'] == 'off'
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP and not is_already_off:
            try:
                LightService.floor_lamp.turn_off()
                status = "succesful"
            except Exception as e:
                print (e)
                status = "error"
        return status

    @staticmethod
    def toggle(light_type: object):
        status = ""
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP:
            try:
                status = LightService.floor_lamp.toggle()
            except Exception as e:
                print (e)
                status = "error"
        return status
    
    @staticmethod
    def adjust_brightness(light_type: object, amount: int):
        status = ""
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP:
            try:
                status = LightService.floor_lamp.set_brightness(amount)
            except Exception as e:
                print(e)
                status = "error"
            return status


if __name__ == "__main__":
    print(LightService.lamp_properties)
    # LightService.turn_off(LightType.LIVING_ROOM_FLOOR_LAMP)

         


 
