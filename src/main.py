"""
Main module for running the cab management portal.
"""

import argparse
import json
import logging
from datetime import datetime
from cab_management.cab_manager import CabManager
from cab_management.city_manager import CityManager
from cab_management.booking_manager import BookingManager
from cab_management.analytics import Analytics
from cab_management.utils import load_initial_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('cab_management')

def display_menu():
    """
    Display the menu options to the user.
    """
    print("\n*** Cab Management System Menu ***")
    print("1. Load initial data from JSON")
    print("2. Register a cab")
    print("3. Update a cab")
    print("4. Book a cab")
    print("5. Show analytics")
    print("6. End trip")
    print("7. Exit")
    print("**********************************")

def load_data(file_path):
    """
    Load data from a JSON file.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: The data loaded from the file.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def register_cabs(cab_manager, cabs):
    """
    Register cabs from data.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        cabs (list): List of cab data dictionaries.
    """
    for cab in cabs:
        cab_manager.registerCab(cab["cabId"], cab["cityId"])
        logger.info(f"Registered cab {cab['cabId']} in city {cab['cityId']}")

def update_cabs(cab_manager, cab_id, state, city_id=None):
    """
    Update a cab's details.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        cab_id (int): The ID of the cab to update.
        state (str): The new state of the cab.
        city_id (int, optional): The new city ID of the cab.
    """
    cab_manager.updateCab(cab_id, state, city_id)
    logger.info(f"Updated cab {cab_id} to state {state} in city {city_id if city_id else 'N/A'}")

def book_cab(booking_manager, city_id):
    """
    Book a cab in a specified city.
    
    Args:
        booking_manager (BookingManager): The BookingManager instance.
        city_id (int): The ID of the city to book a cab in.
    
    Returns:
        Booking: The booking if available; otherwise, None.
    """
    booking_id = booking_manager.bookCab(CabManager.getInstance().cabs, city_id)
    if booking_id:
        booking = booking_manager.bookings.get(booking_id)
        logger.info(f"Booking {booking.bookingId} added for cab {booking.cab.cabId} in city {city_id} at {booking.start_time}")
    else:
        logger.warning("No cabs available.")
    return booking

def end_trip(booking_manager, booking_id):
    """
    End a trip and make the cab available.
    
    Args:
        booking_manager (BookingManager): The BookingManager instance.
        booking_id (int): The ID of the booking to end.
    """
    try:
        booking_manager.endBooking(booking_id)
        logger.info(f"Ended trip for booking ID {booking_id}")
    except ValueError as e:
        logger.error(e)

def show_analytics(cab_manager, city_manager):
    """
    Show analytics for cabs.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        city_manager (CityManager): The CityManager instance.
    """
    cabs = cab_manager.cabs.values()
    for cab in cabs:
        idle_time = Analytics.calculateIdleTime(cab, datetime.min, datetime.now())
        logger.info(f"Cab {cab.cabId} idle time: {idle_time}")
        history = Analytics.getCabHistory(cab)
        logger.info(f"Cab {cab.cabId} history: {history}")

    # Dummy booking data to demonstrate the highDemandCities function
    bookings = cab_manager.getAllBookings()
    high_demand_city, peak_time = Analytics.highDemandCities(bookings)
    logger.info(f"High demand city: {high_demand_city}, Peak time: {peak_time}")

    # Show available cabs in each city
    cities = city_manager.getAllCities()
    for city in cities:
        idle_cabs = [cab for cab in cabs if cab.cityId == city.cityId and cab.state == "IDLE"]
        on_trip_cabs = [cab for cab in cabs if cab.cityId == city.cityId and cab.state == "ON_TRIP"]
        logger.info(f"City: {city.name}, Idle Cabs: {len(idle_cabs)}, On Trip Cabs: {len(on_trip_cabs)}")

def main():
    """
    Main driver function of the cab management program.
    """
    cab_manager = CabManager.getInstance()
    city_manager = CityManager.getInstance()
    booking_manager = BookingManager.getInstance()

    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == '1':
            file_path = input("Enter the path to the JSON file with initial data: ").strip()
            load_initial_data(file_path)
            logger.info("Initial data loaded successfully.")

        elif choice == '2':
            cab_id = int(input("Enter the cab ID to register: ").strip())
            city_id = int(input("Enter the city ID where the cab will be registered: ").strip())
            cab_manager.registerCab(cab_id, city_id)
            logger.info(f"Registered cab {cab_id} in city {city_id}.")

        elif choice == '3':
            cab_id = int(input("Enter the cab ID to update: ").strip())
            state = input("Enter the new state for the cab (IDLE/ON_TRIP): ").strip().upper()
            city_id = input("Enter the new city ID for the cab (optional): ").strip()
            city_id = int(city_id) if city_id else None
            update_cabs(cab_manager, cab_id, state, city_id)

        elif choice == '4':
            city_id = int(input("Enter the city ID where you want to book a cab: ").strip())
            book_cab(booking_manager, city_id)

        elif choice == '5':
            show_analytics(cab_manager, city_manager)

        elif choice == '6':
            booking_id = int(input("Enter the booking ID to end the trip: ").strip())
            end_trip(booking_manager, booking_id)

        elif choice == '7':
            logger.info("Exiting the program.")
            break

        else:
            logger.warning("Invalid option selected. Please try again.")

if __name__ == "__main__":
    main()
