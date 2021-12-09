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
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP:
            LightService.floor_lamp.turn_on()
    
    @staticmethod
    def turn_off(light_type: object):
        if light_type == LightType.LIVING_ROOM_FLOOR_LAMP:
            LightService.floor_lamp.turn_off()

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
    LightService.toggle(LightType.LIVING_ROOM_FLOOR_LAMP)

         


 
