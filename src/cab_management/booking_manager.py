"""
Booking Manager Module
"""

import logging
from datetime import datetime
from .booking import Booking, BookingState

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('cab_management.booking_manager')

class BookingManager:
    """
    Singleton class for managing bookings.
    
    Attributes:
        _instance (BookingManager): The singleton instance of the BookingManager.
    """
    _instance = None

    def __init__(self):
        if BookingManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            BookingManager._instance = self
            self.bookings = []  # List to hold booking data
            logger.info("BookingManager instance created")

    @staticmethod
    def getInstance():
        """
        Get the singleton instance of BookingManager.
        
        Returns:
            BookingManager: The singleton instance of BookingManager.
        """
        if BookingManager._instance is None:
            BookingManager()
            logger.info("BookingManager instance created")
        return BookingManager._instance
    @staticmethod
    def findBestCab(cabs, city):
        """
        Find the best available cab in the given city.
        
        Args:
            cabs (dict): Dictionary of cabs.
            city (str): The city where the cab is needed.
        
        Returns:
            Cab: The best available cab object, or None if no cabs are available.
        """
        logger.info(f"Finding best cab in city {city}")
        idleCabs = [cab for cab in cabs.values() if cab.getCity() == city and cab.getState().__class__.__name__ == "IdleState"]
        if not idleCabs:
            logger.warning(f"No idle cabs available in city {city}")
            return None
        idleCabs.sort(key=lambda cab: sum(1 for time, state in cab.getHistory() if state.__class__.__name__ == "IdleState"), reverse=True)
        selected_cab = idleCabs[0] if idleCabs else None
        if selected_cab:
            selected_cab.setState("ON_TRIP")
            logger.info(f"Selected cab {selected_cab.cabId} for booking in city {city}")
        return selected_cab

    def getAllBookings(self):
        """
        Get all bookings.
        
        Returns:
            list: List of all bookings.
        """
        logger.info("Fetching all bookings")
        return self.bookings
    
    def endBooking(self, booking_id, end_time=None):
        """
        End a booking and make the cab available.

        Args:
            booking_id (int): The ID of the booking to end.
            end_time (datetime, optional): The timestamp when the trip ends. If None, current time will be used.
        """
        logger.info(f"Ending booking with ID {booking_id}")
        if booking_id in self.bookings:
            booking = self.bookings[booking_id]
            cab = booking.cab
            cab.setState("IDLE")
            booking.change_state(BookingState.COMPLETED)
            booking.end_time = end_time if end_time else datetime.now()
            logger.info(f"Booking with ID {booking_id} ended at {booking.end_time} and cab {cab.cabId} set to IDLE")
        else:
            logger.error(f"Booking ID {booking_id} not found.")
            raise ValueError(f"Booking ID {booking_id} not found.")

    def bookCab(self, cabs, city, start_time=None):
        """
        Book a cab in the specified city.
        
        Args:
            cabs (dict): Dictionary of cabs.
            city (str): The city where the cab is needed.
            start_time (datetime, optional): The timestamp when the trip starts. If None, current time will be used.
        
        Returns:
            int: The booking ID of the booked cab, or None if no cabs are available.
        """
        try:
            # Start transaction
            logger.info("Starting transaction for booking a cab")

            # Step 1: Find the best available cab
            best_cab = self.findBestCab(cabs, city)
            if not best_cab:
                logger.warning("No cabs available for booking")
                return None
            
            # Step 2: Reserve the cab
            best_cab.setState("RESERVED")
            logger.info(f"Cab {best_cab.cabId} reserved")
            
            # Step 3: Create a booking for the cab
            booking = Booking(best_cab, city, start_time=start_time)
            self.bookings.append(booking)
            logger.info(f"Booking created with ID {booking.bookingId} for cab {best_cab.cabId}")
            
            # Step 4: Change the state to WAITING_FOR_CUSTOMER
            booking.change_state(BookingState.WAITING_FOR_CUSTOMER)
            logger.info(f"Cab {best_cab.cabId} state changed to WAITING_FOR_CUSTOMER")
            
            # Step 5: Change the state to ON_TRIP
            booking.change_state(BookingState.TRIP_STARTED)
            best_cab.setState("ON_TRIP")
            logger.info(f"Cab {best_cab.cabId} state changed to ON_TRIP")
            
            # Step 6: Return the booking ID
            logger.info("Transaction completed successfully")
            return booking.bookingId

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return None
