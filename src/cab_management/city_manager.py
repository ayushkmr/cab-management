"""
City Manager Module
"""

from .city import City
import logging

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
            logging.info("CityManager instance created.")

    @staticmethod
    def getInstance():
        """
        Get the singleton instance of CityManager.
        
        Returns:
            CityManager: The singleton instance of CityManager.
        """
        if CityManager._instance is None:
            CityManager()
            logging.info("CityManager instance created through getInstance.")
        return CityManager._instance

    def addCity(self, cityId, name):
        """
        Add a new city.
        
        Args:
            cityId (int): Unique identifier for the city.
            name (str): Name of the city.
        """
        self.cities[cityId] = City(cityId, name)
        logging.info(f"City added: ID={cityId}, Name={name}")

    def getCity(self, cityId):
        """
        Get details of a city by cityId.
        
        Args:
            cityId (int): Unique identifier for the city.
        
        Returns:
            City: The city object corresponding to the cityId.
        """
        city = self.cities.get(cityId)
        if city:
            logging.info(f"Retrieved city: ID={cityId}, Name={city.name}")
        else:
            logging.warning(f"City with ID={cityId} not found.")
        return city
    
    def getAllCities(self):
        """
        Get all cities.
        
        Returns:
            list: List of all city objects.
        """
        cities = list(self.cities.values())
        logging.info(f"Retrieved all cities: Count={len(cities)}")
        return cities

    def addCabToCity(self, cab):
        """
        Add a cab to the corresponding city.
        
        Args:
            cab (Cab): The cab object to be added.
        """
        city = self.getCity(cab.cityId)
        if city:
            city.addCab(cab)
            logging.info(f"Cab added to city: Cab ID={cab.cabId}, City ID={cab.cityId}")
        else:
            logging.warning(f"Cannot add cab to city: City ID={cab.cityId} not found.")
    
    def removeCabFromCity(self, cab):
        """
        Remove a cab from the corresponding city.
        
        Args:
            cab (Cab): The cab object to be removed.
        """
        city = self.getCity(cab.cityId)
        if city:
            city.removeCab(cab.cabId)
            logging.info(f"Cab removed from city: Cab ID={cab.cabId}, City ID={cab.cityId}")
        else:
            logging.warning(f"Cannot remove cab from city: City ID={cab.cityId} not found.")

    def getAllCabsInCity(self, cityId):
        """
        Get all cabs in a given city.
        
        Args:
            cityId (int): The ID of the city.
        
        Returns:
            list: List of all cabs in the city.
        """
        city = self.getCity(cityId)
        cabs = city.getCabs() if city else []
        logging.info(f"Retrieved all cabs in city: City ID={cityId}, Count={len(cabs)}")
        return cabs
    
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
        cabs = city.getCabsByState(state) if city else []
        logging.info(f"Retrieved cabs in city by state: City ID={cityId}, State={state}, Count={len(cabs)}")
        return cabs

    def removeCity(self, cityId):
        """
        Remove a city if it has no associated cabs.
        
        Args:
            cityId (int): The ID of the city to be removed.
        
        Returns:
            bool: True if the city was removed, False otherwise.
        """
        city = self.getCity(cityId)
        if city and not city.getCabs():
            del self.cities[cityId]
            logging.info(f"City with ID {cityId} has been removed.")
            return True
        logging.warning(f"City with ID {cityId} cannot be removed as it has associated cabs.")
        return False
