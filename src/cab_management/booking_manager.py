"""
Booking Manager Module
"""

import logging

from datetime import datetime
import random
from .booking import Booking, BookingState
from .city_manager import CityManager
from .cab import CabState

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
            self.bookings = {}  # Dictionary to hold booking data, booking id -> booking object
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
    def findBestCab(city):
        """
        Find the best available cab in the given city.
        
        Args:
            city (str): The city where the cab is needed.
        
        Returns:
            Cab: The best available cab object, or None if no cabs are available.
        """
        logger.info(f"Finding best cab in city {city}")
        cabs = CityManager.getInstance().getCabsInCityByState(city, CabState.IDLE)  # Get idle cabs directly from CityManager
        logger.info(f"Available cabs in city {city}: {[cab.cabId for cab in cabs]}")
        if not cabs:
            logger.warning(f"No idle cabs available in city {city}")
            return None
        
        for cab in cabs:
            idle_time = cab.getIdleTime()
            logger.info(f"Cab ID: {cab.cabId}, Idle Time: {idle_time} seconds")
        # Sort cabs based on idle time
        cabs.sort(key=lambda cab: cab.getIdleTime(), reverse=True)
        
        for cab in cabs:
            idle_time = cab.getIdleTime()
            logger.info(f"Cab ID: {cab.cabId}, Idle Time: {idle_time} seconds")
            
        # If there are multiple cabs with the same idle time, randomly select one
        max_idle_time = cabs[0].getIdleTime()
        best_cabs = [cab for cab in cabs if cab.getIdleTime() == max_idle_time]
        
        if best_cabs:
            selected_cab = random.choice(best_cabs)
            logger.info(f"Selected cab {selected_cab.cabId} from best cabs")
        else:
            selected_cab = None
            logger.warning("No cabs were selected as best cabs list is empty")
        
        return selected_cab

    def addBooking(self, booking):
        """
        Add a booking to the bookings dictionary.
        
        Args:
            booking (Booking): The booking object to be added.
        """
        logger.info(f"Booking {booking.bookingId} added for cab {booking.cab.cabId} in city {booking.city.cityId} at {booking.start_time}")
        self.bookings[booking.bookingId] = booking

    def getBookings(self):
        """
        Get the bookings dictionary.
        
        Returns:
            dict: Dictionary of bookings with booking ID as key and booking object as value.
        """
        logger.info("Fetching bookings")
        return self.bookings
        
    def getAllBookings(self):
        """
        Get all bookings.
        
        Returns:
            list: List of all bookings.
        """
        logger.info("Fetching all bookings")
        return list(self.bookings.values())
    
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
            cab.setState(CabState.IDLE, end_time)  # Set state using the CabState enum
            booking.change_state(BookingState.COMPLETED)
            booking.end_time = end_time if end_time else datetime.now()
            logger.info(f"Booking with ID {booking_id} ended at {booking.end_time} and cab {cab.cabId} set to IDLE")
            return True  # Return True for successful operation
        else:
            logger.error(f"Booking ID {booking_id} not found.")
            return False  # Return False if booking ID is not found

    def bookCab(self, city, start_time=None):
        """
        Book a cab in the specified city.
        
        Args:
            city (str): The city where the cab is needed.
            start_time (datetime, optional): The timestamp when the trip starts. If None, current time will be used.
        
        Returns:
            int: The booking ID of the booked cab, or None if no cabs are available.
        """
        try:
            # Start transaction
            logger.info("Starting transaction for booking a cab")

            # Step 1: Find the best available cab
            best_cab = self.findBestCab(city)
            if not best_cab:
                logger.warning("No cabs available for booking")
                return None
            
            # Step 2: Reserve the cab
            best_cab.setState(CabState.RESERVED, start_time)  # Set state using the CabState enum
            logger.info(f"Cab {best_cab.cabId} reserved")
            
            # Step 3: Create a booking for the cab
            booking = Booking(best_cab, city, start_time=start_time)
            self.addBooking(booking)  # Use the addBooking method to add the booking
            best_cab.addBooking(booking.bookingId)  # Add booking to cab
            logger.info(f"Booking created with ID {booking.bookingId} for cab {best_cab.cabId}")
            
            # Step 4: Change the state to WAITING_FOR_CUSTOMER
            booking.change_state(BookingState.WAITING_FOR_CUSTOMER)
            logger.info(f"Cab {best_cab.cabId} state changed to WAITING_FOR_CUSTOMER")
            
            # Step 5: Change the state to ON_TRIP
            booking.change_state(BookingState.TRIP_STARTED)
            best_cab.setState(CabState.ON_TRIP, start_time)  # Set state using the CabState enum
            logger.info(f"Cab {best_cab.cabId} state changed to ON_TRIP")
            
            # Step 6: Return the booking ID
            logger.info("Transaction completed successfully")
            return booking.bookingId

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return None

    def bookOldCab(self, cab, city, start_time=None):
        """
        Book an old cab using the specified cab ID.
        
        Args:
            cab_id (int): The ID of the cab to be booked.
            city (str): The city where the cab is needed.
            start_time (datetime, optional): The timestamp when the trip starts. If None, current time will be used.
        
        Returns:
            int: The booking ID of the booked cab, or None if the cab is not available.
        """
        try:
            # Start transaction
            logger.info("Starting transaction for booking an old cab")
            
            # Step 1: Reserve the cab
            cab.setState(CabState.RESERVED, start_time)  # Set state using the CabState enum
            logger.info(f"Cab {cab.cabId} reserved")
            
            # Step 2: Create a booking for the cab
            booking = Booking(cab, city, start_time=start_time)
            self.addBooking(booking)  # Use the addBooking method to add the booking
            cab.addBooking(booking.bookingId)  # Add booking to cab
            logger.info(f"Booking created with ID {booking.bookingId} for cab {cab.cabId}")
            
            # Step 3: Change the state to WAITING_FOR_CUSTOMER
            booking.change_state(BookingState.WAITING_FOR_CUSTOMER)
            logger.info(f"Cab {cab.cabId} state changed to WAITING_FOR_CUSTOMER")
            
            # Step 4: Change the state to ON_TRIP
            booking.change_state(BookingState.TRIP_STARTED)
            cab.setState(CabState.ON_TRIP, start_time)  # Set state using the CabState enum
            logger.info(f"Cab {cab.cabId} state changed to ON_TRIP")
            
            # Step 5: Return the booking ID
            logger.info("Transaction completed successfully")
            return booking.bookingId

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return None
