"""
Utility functions for Cab Management
"""

import json
from cab_management.cab_manager import CabManager
from cab_management.city_manager import CityManager
from cab_management.booking_manager import BookingManager

def load_initial_data(file_path):
    """
    Load initial data from a JSON file.
    
    Args:
        file_path (str): The path to the JSON file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    cab_manager = CabManager.getInstance()
    city_manager = CityManager.getInstance()
    booking_manager = BookingManager.getInstance()

    for city in data['cities']:
        city_manager.addCity(city['cityId'], city['name'])

    for cab in data['cabs']:
        cab_manager.registerCab(cab['cabId'], cab['cityId'])
        cab_manager.updateCab(cab['cabId'], cab['cabState'], cab['cityId'])

    for booking in data['bookings']:
        booking_manager.addBooking(booking['bookingId'], booking['cabId'], booking['cityId'], booking['timestamp'])
