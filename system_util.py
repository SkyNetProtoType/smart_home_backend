import psutil
from datetime import datetime

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



if __name__ == "__main__":
    # print(SystemUtil.get_battery_info())
    print(SystemUtil.date_diff_from_now("2021-11-16 15:26:00.640397"))