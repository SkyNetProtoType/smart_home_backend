import psutil
import asyncio
from datetime import datetime
from kasa import SmartPlug
from decouple import config

SMART_BULB = config("TABLET_SMART_PLUG")

class SystemUtil:

    @staticmethod
    def get_battery_info():
        battery = psutil.sensors_battery()
        return {
            'batteryPercent': battery.percent,
            'isPluggedIn': battery.power_plugged
        }

    @staticmethod
    def date_diff_from_now(str_timestamp: str): 
        current_moment = datetime.now()
        timestamp = datetime.strptime(str_timestamp, "%Y-%m-%d %H:%M:%S.%f")
        date_diff = current_moment - timestamp
        return date_diff.days

    @staticmethod
    async def toggle_smart_plug(state: str, ip_address = SMART_BULB):
        connectivity = ""
        plug = SmartPlug(ip_address)
        try:
            await plug.update()
        except Exception:
            connectivity = "error connecting to " + plug.alias + '...'
            return connectivity

        if "on" == state.lower():
            if plug.is_on:
                connectivity = "already activated"
            else:
                try:
                    await plug.turn_on()
                    connectivity = "activated"   
                except Exception:
                    connectivity = "error turning on plug..."         
        elif "off" == state.lower():
            if plug.is_off:
                connectivity = "already deactivated"
            else:
                try:
                    await plug.turn_off()
                    connectivity = "deactivated"
                except Exception:
                    connectivity = "error turning off plug..."
        
        return connectivity



if __name__ == "__main__":
    # print(SystemUtil.get_battery_info())
    # print(SystemUtil.date_diff_from_now("2021-11-16 15:26:00.640397"))
    print(asyncio.run(SystemUtil.toggle_smart_plug(input("Enter 'on'/'off': "))))