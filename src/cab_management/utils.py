"""
Utility functions for Cab Management
"""

import datetime
import json
import logging
from cab_management.cab_manager import CabManager
from cab_management.city_manager import CityManager
from cab_management.booking_manager import BookingManager
from cab_management.booking import Booking, BookingState
from cab_management.cab import CabState

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('cab_management.utils')

INITIAL_DATA_PATH = "data/initial_data.json"

def load_initial_data(file_path=None):
    """
    Load initial data from a JSON file.
    
    Args:
        file_path (str): The path to the JSON file. If None or empty, use INITIAL_DATA_PATH.
    """
    if not file_path:
        file_path = INITIAL_DATA_PATH

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        logger.info(f"Initial data loaded successfully from {file_path}")
    except Exception as e:
        logger.error(f"Failed to load initial data from {file_path}: {e}")
        return

    cab_manager = CabManager.getInstance()
    city_manager = CityManager.getInstance()
    booking_manager = BookingManager.getInstance()

    try:
        for city in data['cities']:
            city_manager.addCity(city['cityId'], city['name'])
            logger.info(f"City {city['name']} with ID {city['cityId']} added.")

        for cab in data['cabs']:
            cab_manager.registerCab(cab['cabId'], cab['cityId'])
            cab_manager.updateCab(cab['cabId'], cab['cabState'], cab['cityId'])
            logger.info(f"Cab {cab['cabId']} registered in city {cab['cityId']} with state {cab['cabState']}.")

        for booking in data['bookings']:
            cab_id = booking['cabId']
            city_id = booking['cityId']
            start_time = booking['start_time']
            end_time = booking.get('end_time', None)
            add_old_booking(booking_manager, cab_manager, city_manager, cab_id, city_id, start_time, end_time)
            logger.info(f"Booking added for cab {cab_id} in city {city_id} from {start_time} to {end_time}.")

        logger.info("All initial data processed successfully.")
    except Exception as e:
        logger.error(f"Error processing initial data: {e}")

def add_booking(city_id, start_time=None):
    """
    Add a new booking to the booking list using individual parameters.
    
    Args:
        city_id (int): The ID of the city.
        start_time (str, optional): The start time of the booking. If None, current time will be used.
    """
    booking_manager = BookingManager.getInstance()
    cab_manager = CabManager.getInstance()
    
    # Book a cab in the specified city with the given start time
    booking_id = booking_manager.bookCab(cab_manager.cabs, city_id, start_time)
    
    if booking_id is not None:
        booking = booking_manager.bookings.get(booking_id)
        logger.info(f"Booking {booking.bookingId} added for cab {booking.cab.cabId} in city {city_id} at {booking.start_time}")
    else:
        logger.warning(f"No cabs available for booking in city {city_id}")

def end_trip_with_timestamp(booking_id, end_time=None):
    """
    End a trip and make the cab available with a specified end time.
    
    Args:
        booking_id (int): The ID of the booking to end.
        end_time (str, optional): The end time when the trip ended. If None, current time will be used.
    """
    booking_manager = BookingManager.getInstance()
    
    try:
        booking_manager.endBooking(booking_id, end_time)
        logger.info(f"Booking with ID {booking_id} ended at {end_time if end_time else datetime.datetime.now()}")
    except ValueError as e:
        logger.error(e)

def add_old_booking(booking_manager, cab_manager, city_manager, cab_id, city_id, start_time, end_time=None):
    """
    Add an old booking to the booking list, either completed or ongoing.
    
    Args:
        booking_manager (BookingManager): The BookingManager instance.
        cab_manager (CabManager): The CabManager instance.
        city_manager (CityManager): The CityManager instance.
        cab_id (int): The ID of the cab.
        city_id (int): The ID of the city.
        start_time (str): The start time of the booking.
        end_time (str, optional): The end time of the booking. If None, the booking is considered ongoing.
    """
    cab = cab_manager.getCab(cab_id)
    city = city_manager.getCity(city_id)

    if cab and city:
        state = BookingState.COMPLETED if end_time else BookingState.TRIP_STARTED
        booking = Booking(cab, city, state=state, start_time=start_time, end_time=end_time)
        booking_manager.addBooking(booking)
        
        cab.setState((CabState.IDLE if state == BookingState.COMPLETED else CabState.ON_TRIP), 
                     end_time if end_time else start_time)
        logger.info(f"Old booking {booking.bookingId} added for cab {cab_id} in city {city_id} from {start_time} to {end_time if end_time else 'ongoing'}")
    else:
        logger.warning(f"Cab {cab_id} or city {city_id} not found. Cannot add old booking.")


# Example usage
if __name__ == "__main__":
    load_initial_data()
