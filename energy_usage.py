
class EnergyUsage:

    def __init__(self, dates, usage, cost) -> None:
        self._dates = dates
        self._usage = usage
        self._cost = cost

    def get_dates(self):
        return self._dates

    def set_dates(self, new_dates):
        self._dates = new_dates
    
    def get_usage(self):
        return self._usage

    def set_usage(self, new_usage):
        self._dates = new_usage

    def get_cost(self):
        return self._cost

    def set_cost(self, new_cost):
        self._dates = new_cost