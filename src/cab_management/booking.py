"""
Booking Module
"""

from datetime import datetime
from enum import Enum
from .city import City
from .city_manager import CityManager

class BookingState(Enum):
    BOOKED = "BOOKED"
    WAITING_FOR_CUSTOMER = "WAITING_FOR_CUSTOMER"
    TRIP_STARTED = "TRIP_STARTED"
    CANCELLED = "CANCELLED"
    WAITING_FOR_PAYMENT = "WAITING_FOR_PAYMENT"
    COMPLETED = "COMPLETED"

class Booking:
    """
    Represents a Booking.
    
    Attributes:
        bookingId (int): Unique identifier for the booking.
        cab (Cab): The cab assigned for the booking.
        city (City): The city where the booking is made.
        state (BookingState): The current state of the booking.
        start_time (datetime): The timestamp when the trip starts.
        end_time (datetime): The timestamp when the trip ends.
    """
    _booking_counter = 0

    @classmethod
    def _get_next_booking_id(cls):
        cls._booking_counter += 1
        return cls._booking_counter

    def __init__(self, cab, city, state=BookingState.BOOKED, start_time=None, end_time=None):
        self.bookingId = Booking._get_next_booking_id()
        self.cab = cab
        
        # Check if city is an instance of City or an integer
        if isinstance(city, City):
            self.city = city
        elif isinstance(city, int):
            city_manager = CityManager.getInstance()
            city_obj = city_manager.getCity(city)  # Get the city object using city_id
            if city_obj is None:
                raise ValueError(f"Invalid city ID: {city}")
            self.city = city_obj
        else:
            raise ValueError(f"Invalid city type: {type(city)}. Must be City object or city ID (int).")
        
        self.state = state
        self.start_time = start_time if start_time else datetime.now()
        self.end_time = end_time

    def change_state(self, new_state):
        """
        Change the state of the booking.
        
        Args:
            new_state (BookingState): The new state of the booking.
        """
        if not isinstance(new_state, BookingState):
            raise ValueError(f"Invalid state: {new_state}")
        self.state = new_state
