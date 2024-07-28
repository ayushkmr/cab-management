"""
Cab Module
"""

from datetime import datetime
import logging
from .state_manager import StateManager

class Cab:
    """
    Represents a Cab.
    
    Attributes:
        cabId (int): Unique identifier for the cab.
        location (str): Current location of the cab.
        state (State): Current state of the cab.
        history (list): List of tuples containing the timestamp and state.
    """
    def __init__(self, cabId, location):
        self.cabId = cabId
        self.location = location
        self.state = StateManager.getState("IDLE")
        self.history = [(datetime.now(), self.state)]
        logging.info(f"Cab {self.cabId} initialized at location {self.location} with state {self.state.__class__.__name__}")

    def setState(self, state):
        """
        Set the state of the cab and record the timestamp.
        
        Args:
            state (str): The new state of the cab.
        """
        self.state = StateManager.getState(state)
        self.history.append((datetime.now(), self.state))
        logging.info(f"Cab {self.cabId} state changed to {self.state.__class__.__name__}")

    def setLocation(self, location):
        """
        Set the location of the cab.
        
        Args:
            location (str): The new location of the cab.
        """
        self.location = location
        logging.info(f"Cab {self.cabId} location changed to {self.location}")

    def getState(self):
        """
        Get the current state of the cab.
        
        Returns:
            State: The current state of the cab.
        """
        return self.state

    def getLocation(self):
        """
        Get the current location of the cab.
        
        Returns:
            str: The current location of the cab.
        """
        return self.location

    def getHistory(self):
        """
        Get the state history of the cab.
        
        Returns:
            list: List of tuples containing the timestamp and state.
        """
        return self.history
