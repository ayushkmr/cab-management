"""
Cab Module
"""

from datetime import datetime
import logging
from .state_manager import StateManager
from .city import City

class Cab:
    """
    Represents a Cab.
    
    Attributes:
        cabId (int): Unique identifier for the cab.
        cityId (int): Current city ID of the cab.
        state (State): Current state of the cab.
        history (list): List of tuples containing the timestamp and state.
    """
    def __init__(self, cabId, cityId):
        self.cabId = cabId
        self.cityId = cityId
        self.state = StateManager.getState("IDLE")
        self.history = [(datetime.now(), self.state)]
        logging.info(f"Cab {self.cabId} initialized in city ID {self.cityId} with state {self.state.__class__.__name__}")

    def setState(self, state):
        """
        Set the state of the cab and record the timestamp.
        
        Args:
            state (str): The new state of the cab.
        """
        self.state = StateManager.getState(state)
        self.history.append((datetime.now(), self.state))
        logging.info(f"Cab {self.cabId} state changed to {self.state.__class__.__name__}")

    def setCity(self, cityId):
        """
        Set the city ID of the cab.
        
        Args:
            cityId (int): The new city ID of the cab.
        """
        self.cityId = cityId
        logging.info(f"Cab {self.cabId} city ID changed to {self.cityId}")

    def getState(self):
        """
        Get the current state of the cab.
        
        Returns:
            State: The current state of the cab.
        """
        return self.state

    def getCity(self):
        """
        Get the current city ID of the cab.
        
        Returns:
            int: The current city ID of the cab.
        """
        return self.cityId

    def getHistory(self):
        """
        Get the state history of the cab.
        
        Returns:
            list: List of tuples containing the timestamp and state.
        """
        return self.history
