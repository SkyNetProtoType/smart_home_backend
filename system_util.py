import psutil

class SystemUtil:

    @staticmethod
    def get_battery_info():
        battery = psutil.sensors_battery()
        return {
            'batteryPercent': battery.percent,
            'isPluggedIn': battery.power_plugged
        }


if __name__ == "__main__":
    print(SystemUtil.get_battery_info())