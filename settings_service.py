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
        'activate_sunset_routine': True if input("Sunset settings: Enter 'Y'/'N': ").lower() == "y" else False,
        'activate_hourly_weather_update': True,
        'activate_battery_info': True if input("Battery info settings: Enter 'Y'/'N': ").lower() == "y" else False, 
        'activate_energy_usage_chart': True, 
        'twelve_minutes': 720000, 
        'fifteen_minutes': 900000, 
        'one_hour': 3600000
    }
    print()
    SettingsService.update_dashboard_settings(updated_settings)
    print("After updating settings:")
    print(SettingsService.get_dashboard_settings())

