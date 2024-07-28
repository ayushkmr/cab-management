"""
Booking Module
"""

from datetime import datetime

class Booking:
    """
    Represents a Booking.
    
    Attributes:
        bookingId (int): Unique identifier for the booking.
        cab (Cab): The cab assigned for the booking.
        city (City): The city where the booking is made.
        time (datetime): The timestamp when the booking is made.
    """
    def __init__(self, bookingId, cab, city):
        self.bookingId = bookingId
        self.cab = cab
        self.city = city
        self.time = datetime.now()
