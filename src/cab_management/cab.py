"""
Cab Module
"""

from datetime import datetime, timedelta
import logging
from enum import Enum

class CabState(Enum):
    IDLE = "IDLE"
    RESERVED = "RESERVED"
    ON_TRIP = "ON_TRIP"

class Cab:
    """
    Represents a Cab.
    
    Attributes:
        cabId (int): Unique identifier for the cab.
        cityId (int): Current city ID of the cab.
        state (CabState): Current state of the cab.
        history (list): List of tuples containing the timestamp and state.
        bookings (list): List of booking IDs associated with the cab.
    """
    def __init__(self, cabId, cityId):
        self.cabId = cabId
        self.cityId = cityId
        self.state = CabState.IDLE
        self.history = [(datetime.now(), self.state)]
        self.bookings = []  # List to store booking IDs
        logging.info(f"Cab {self.cabId} initialized in city ID {self.cityId} with state {self.state}")

    def setState(self, state, timestamp=None):
        """
        Set the state of the cab and record the timestamp.
        
        Args:
            state (Union[CabState, str]): The new state of the cab, can be a CabState or a string.
            timestamp (datetime, optional): The timestamp to record. If None, the current time will be used.
        """
        if isinstance(state, str):
            try:
                state = CabState[state]  # Convert string to CabState
            except KeyError:
                raise ValueError(f"Invalid state string: {state}")
        elif not isinstance(state, CabState):
            raise ValueError(f"Invalid state: {state}")
        
        if self.state != state:  # Only change state if it's different
            self.state = state
            if timestamp is None:
                timestamp = datetime.now()  # Use current time if no timestamp is provided
            self.history.append((timestamp, self.state))
            logging.info(f"Cab {self.cabId} state changed to {self.state}")

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
            CabState: The current state of the cab.
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

    def addBooking(self, bookingId):
        """
        Add a booking ID to the cab's booking history.
        
        Args:
            bookingId (int): The ID of the booking to add.
        """
        self.bookings.append(bookingId)
        logging.info(f"Booking {bookingId} added to cab {self.cabId}")

    def getBookings(self):
        """
        Get the list of booking IDs associated with the cab.
        
        Returns:
            list: List of booking IDs.
        """
        return self.bookings

    def getIdleTime(self):
        """
        Calculate the total idle time of the cab.
        
        Returns:
            int: The total idle time in seconds.
        """
        total_idle_time = timedelta(0)
        current_time = datetime.now()
        previous_time = self.history[0][0]

        for timestamp, state in self.history:
            if state == CabState.IDLE:
                total_idle_time += timestamp - previous_time
            previous_time = timestamp
        
        if self.state == CabState.IDLE:
            total_idle_time += current_time - previous_time
        
        return int(total_idle_time.total_seconds())
