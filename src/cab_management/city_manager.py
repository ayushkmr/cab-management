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
    
    def getAllCities(self):
        """
        Get all cities.
        
        Returns:
            list: List of all city objects.
        """
        return list(self.cities.values())

    def addCabToCity(self, cab):
        """
        Add a cab to the corresponding city.
        
        Args:
            cab (Cab): The cab object to be added.
        """
        city = self.getCity(cab.cityId)
        if city:
            city.addCab(cab)
    
    def removeCabFromCity(self, cab):
        """
        Remove a cab from the corresponding city.
        
        Args:
            cab (Cab): The cab object to be removed.
        """
        city = self.getCity(cab.cityId)
        if city:
            city.removeCab(cab.cabId)

    def getAllCabsInCity(self, cityId):
        """
        Get all cabs in a given city.
        
        Args:
            cityId (int): The ID of the city.
        
        Returns:
            list: List of all cabs in the city.
        """
        city = self.getCity(cityId)
        return city.getAllCabs() if city else []
    
    def getCabsInCityByState(self, cityId, state):
        """
        Get all cabs in a given city with a specific state.
        
        Args:
            cityId (int): The ID of the city.
            state (CabState): The state to filter cabs by.
        
        Returns:
            list: List of cabs in the city with the given state.
        """
        city = self.getCity(cityId)
        return city.getCabsByState(state) if city else []
