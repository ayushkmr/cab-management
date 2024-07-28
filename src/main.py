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
    print("6. Exit")
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

def book_cab(cab_manager, city_id):
    """
    Book a cab in a specified city.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        city_id (int): The ID of the city to book a cab in.
    
    Returns:
        Cab: The booked cab if available; otherwise, None.
    """
    booked_cab = cab_manager.bookCab(city_id)
    if booked_cab:
        logger.info(f"Cab {booked_cab.cabId} booked successfully.")
    else:
        logger.warning("No cabs available.")
    return booked_cab

def show_analytics(cab_manager):
    """
    Show analytics for cabs.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
    """
    cabs = cab_manager.cabs.values()
    for cab in cabs:
        idle_time = Analytics.calculateIdleTime(cab, None, datetime.now())
        logger.info(f"Cab {cab.cabId} idle time: {idle_time}")
        history = Analytics.getCabHistory(cab)
        logger.info(f"Cab {cab.cabId} history: {history}")

    # Dummy booking data to demonstrate the highDemandCities function
    bookings = cab_manager.getAllBookings()
    high_demand_city, peak_time = Analytics.highDemandCities(bookings)
    logger.info(f"High demand city: {high_demand_city}, Peak time: {peak_time}")

def main():
    """
    Main driver function of the cab management program.
    """
    cab_manager = CabManager.getInstance()
    city_manager = CityManager.getInstance()
    booking_manager = BookingManager.getInstance()

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

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
            book_cab(cab_manager, city_id)

        elif choice == '5':
            show_analytics(cab_manager)

        elif choice == '6':
            logger.info("Exiting the program.")
            break

        else:
            logger.warning("Invalid option selected. Please try again.")

if __name__ == "__main__":
    main()
