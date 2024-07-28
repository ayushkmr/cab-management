"""
City Manager Module
"""

from .city import City

class CityManager:
    """
    Singleton class for managing cities.
    
    Attributes:
        _instance (CityManager): The singleton instance of the CityManager.
        cities (dict): Dictionary mapping city IDs to City objects.
    """
    _instance = None

    def __init__(self):
        if CityManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CityManager._instance = self
            self.cities = {}  # cityId -> City object

    @staticmethod
    def getInstance():
        """
        Get the singleton instance of CityManager.
        
        Returns:
            CityManager: The singleton instance of CityManager.
        """
        if CityManager._instance is None:
            CityManager()
        return CityManager._instance

    def addCity(self, cityId, name):
        """
        Add a new city.
        
        Args:
            cityId (int): Unique identifier for the city.
            name (str): Name of the city.
        """
        self.cities[cityId] = City(cityId, name)

    def getCity(self, cityId):
        """
        Get details of a city by cityId.
        
        Args:
            cityId (int): Unique identifier for the city.
        
        Returns:
            City: The city object corresponding to the cityId.
        """
        return self.cities.get(cityId)
