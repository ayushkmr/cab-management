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

    def registerCab(self, cabId, cityId):
        """
        Register a new cab.
        
        Args:
            cabId (int): Unique identifier for the cab.
            cityId (int): Initial city ID of the cab.
        """
        self.cabs[cabId] = Cab(cabId, cityId)
        logging.info(f"Cab {cabId} registered in city ID {cityId}")

    def updateCab(self, cabId, state=None, cityId=None):
        """
        Update the state or location of an existing cab.
        
        Args:
            cabId (int): Unique identifier for the cab.
            state (str, optional): The new state of the cab.
            cityId (int, optional): The new city ID of the cab.
        """
        if cabId in self.cabs:
            if state:
                self.cabs[cabId].setState(state)
            if cityId:
                self.cabs[cabId].setCity(cityId)
            logging.info(f"Cab {cabId} updated with state {state} and city ID {cityId}")

    def getCab(self, cabId):
        """
        Get details of a cab by cabId.
        
        Args:
            cabId (int): Unique identifier for the cab.
        
        Returns:
            Cab: The cab object corresponding to the cabId.
        """
        return self.cabs.get(cabId)


    def getAllBookings(self):
        """
        Get all bookings for cabs.
        
        Returns:
            list: List of all bookings.
        """
        return BookingManager.getInstance().getAllBookings()

