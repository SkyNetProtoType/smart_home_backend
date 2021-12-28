import json

class SettingsService:

    @staticmethod
    def get_dashboard_settings() -> dict:
        with open('settings.json') as file:
            return json.load(file)
    
    @staticmethod
    def update_dashboard_settings(updated_settings: dict):
        with open("settings.json", 'w') as file:
            json.dump(updated_settings, file)




if __name__ == "__main__":
    print ("Before updating settings:")
    print(SettingsService.get_dashboard_settings())
    print()
    updated_settings = {
        'sunset_routine': True if input("Sunset settings: Enter 'Y'/'N': ").lower() == "y" else False,
        "battery_update_time": 720000,
        "weather_update_time": 3600000,
        "lamp_brightness":85,
    }
    print()
    SettingsService.update_dashboard_settings(updated_settings)
    print("After updating settings:")
    print(SettingsService.get_dashboard_settings())

