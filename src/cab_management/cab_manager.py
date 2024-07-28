"""
Cab Manager Module
"""

import logging
from .cab import Cab
from .state_manager import StateManager
from .booking_manager import BookingManager

class CabManager:
    """
    Singleton class for managing cabs.
    
    Attributes:
        _instance (CabManager): The singleton instance of the CabManager.
        cabs (dict): Dictionary mapping cab IDs to Cab objects.
    """
    _instance = None

    def __init__(self):
        if CabManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CabManager._instance = self
            self.cabs = {}  # cabId -> Cab object

    @staticmethod
    def getInstance():
        """
        Get the singleton instance of CabManager.
        
        Returns:
            CabManager: The singleton instance of CabManager.
        """
        if CabManager._instance is None:
            CabManager()
        return CabManager._instance

    def registerCab(self, cabId, city):
        """
        Register a new cab.
        
        Args:
            cabId (int): Unique identifier for the cab.
            city (str): Initial city location of the cab.
        """
        self.cabs[cabId] = Cab(cabId, city)
        logging.info(f"Cab {cabId} registered in city {city}")

    def updateCab(self, cabId, state=None, city=None):
        """
        Update the state or location of an existing cab.
        
        Args:
            cabId (int): Unique identifier for the cab.
            state (str, optional): The new state of the cab.
            city (str, optional): The new city location of the cab.
        """
        if cabId in self.cabs:
            if state:
                self.cabs[cabId].setState(state)
            if city:
                self.cabs[cabId].setLocation(city)
            logging.info(f"Cab {cabId} updated with state {state} and city {city}")

    def bookCab(self, city):
        """
        Book a cab in the specified city.
        
        Args:
            city (str): The city where the cab is to be booked.
        
        Returns:
            Cab: The booked cab object, or None if no cabs are available.
        """
        booked_cab = BookingManager.findBestCab(self.cabs, city)
        if booked_cab:
            logging.info(f"Cab {booked_cab.cabId} booked in city {city}")
        return booked_cab
