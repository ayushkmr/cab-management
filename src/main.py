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
    print("2. Cab Management")
    print("3. Booking Management")
    print("4. Show Analytics")
    print("5. Exit")
    print("**********************************")

def cab_management_menu():
    """
    Display the cab management menu options to the user.
    """
    print("\n*** Cab Management Menu ***")
    print("1. Register a cab")
    print("2. Update a cab")
    print("3. Show cab booking history")
    print("4. Show cab state change history")
    print("5. Back to main menu")
    print("****************************")

def booking_management_menu():
    """
    Display the booking management menu options to the user.
    """
    print("\n*** Booking Management Menu ***")
    print("1. Book a cab")
    print("2. End a trip")
    print("3. Back to main menu")
    print("*******************************")

def load_data(file_path):
    """
    Load data from a JSON file.
    
    Args:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: The data loaded from the file.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        return None

def register_cabs(cab_manager, cabs):
    """
    Register cabs from data.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        cabs (list): List of cab data dictionaries.
    """
    try:
        for cab in cabs:
            cab_manager.registerCab(cab["cabId"], cab["cityId"])
            logger.info(f"Registered cab {cab['cabId']} in city {cab['cityId']}")
    except Exception as e:
        logger.error(f"Error registering cabs: {e}")

def update_cabs(cab_manager, cab_id, state, city_id=None):
    """
    Update a cab's details.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        cab_id (int): The ID of the cab to update.
        state (str): The new state of the cab.
        city_id (int, optional): The new city ID of the cab.
    """
    try:
        cab_manager.updateCab(cab_id, state, city_id)
        logger.info(f"Updated cab {cab_id} to state {state} in city {city_id if city_id else 'N/A'}")
    except Exception as e:
        logger.error(f"Error updating cab {cab_id}: {e}")

def show_cab_booking_history(cab_manager, cab_id):
    """
    Show the booking history of a cab.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        cab_id (int): The ID of the cab.
    """
    try:
        cab = cab_manager.getCab(cab_id)
        if cab:
            bookings = cab.getBookings()
            if bookings:
                logger.info(f"Cab {cab_id} booking history:")
                for booking_id in bookings:
                    logger.info(f" - Booking ID: {booking_id}")
            else:
                logger.info(f"Cab {cab_id} has no booking history.")
        else:
            logger.warning(f"Cab {cab_id} not found.")
    except Exception as e:
        logger.error(f"Error showing booking history for cab {cab_id}: {e}")

def show_cab_state_change_history(cab_manager, cab_id):
    """
    Show the state change history of a cab.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        cab_id (int): The ID of the cab.
    """
    try:
        cab = cab_manager.getCab(cab_id)
        if cab:
            history = cab.getHistory()
            if history:
                logger.info(f"Cab {cab_id} state change history:")
                for timestamp, state in history:
                    logger.info(f" - {timestamp}: State changed to {state}")
            else:
                logger.info(f"Cab {cab_id} has no state change history.")
        else:
            logger.warning(f"Cab {cab_id} not found.")
    except Exception as e:
        logger.error(f"Error showing state change history for cab {cab_id}: {e}")

def book_cab(booking_manager, city_id):
    """
    Book a cab in a specified city.
    
    Args:
        booking_manager (BookingManager): The BookingManager instance.
        city_id (int): The ID of the city to book a cab in.
    
    Returns:
        Booking: The booking if available; otherwise, None.
    """
    try:
        booking_id = booking_manager.bookCab(city_id)
        if booking_id:
            booking = booking_manager.bookings.get(booking_id)
            logger.info(f"Booking {booking.bookingId} added for cab {booking.cab.cabId} in city {city_id} at {booking.start_time}")
            return booking
        else:
            logger.warning("No cabs available.")
            return None
    except Exception as e:
        logger.error(f"Error while booking cab: {e}")
        return None

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
    except Exception as e:
        logger.error(f"Error ending trip for booking ID {booking_id}: {e}")

def show_analytics(cab_manager, city_manager):
    """
    Show analytics for cabs.
    
    Args:
        cab_manager (CabManager): The CabManager instance.
        city_manager (CityManager): The CityManager instance.
    """
    try:
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
    except Exception as e:
        logger.error(f"Error showing analytics: {e}")

def main():
    """
    Main driver function of the cab management program.
    """
    try:
        cab_manager = CabManager.getInstance()
        city_manager = CityManager.getInstance()
        booking_manager = BookingManager.getInstance()

        while True:
            display_menu()
            choice = input("Select an option (1-5): ").strip()

            if choice == '1':
                file_path = input("Enter the path to the JSON file with initial data: ").strip()
                load_initial_data(file_path)
                logger.info("Initial data loaded successfully.")

            elif choice == '2':
                while True:
                    cab_management_menu()
                    cab_choice = input("Select an option (1-5): ").strip()

                    if cab_choice == '1':
                        cab_id = int(input("Enter the cab ID to register: ").strip())
                        city_id = int(input("Enter the city ID where the cab will be registered: ").strip())
                        cab_manager.registerCab(cab_id, city_id)
                        logger.info(f"Registered cab {cab_id} in city {city_id}.")

                    elif cab_choice == '2':
                        cab_id = int(input("Enter the cab ID to update: ").strip())
                        state = input("Enter the new state for the cab (IDLE/ON_TRIP): ").strip().upper()
                        city_id = input("Enter the new city ID for the cab (optional): ").strip()
                        city_id = int(city_id) if city_id else None
                        update_cabs(cab_manager, cab_id, state, city_id)

                    elif cab_choice == '3':
                        cab_id = int(input("Enter the cab ID to show booking history: ").strip())
                        show_cab_booking_history(cab_manager, cab_id)

                    elif cab_choice == '4':
                        cab_id = int(input("Enter the cab ID to show state change history: ").strip())
                        show_cab_state_change_history(cab_manager, cab_id)

                    elif cab_choice == '5':
                        break

                    else:
                        logger.warning("Invalid option selected. Please try again.")

            elif choice == '3':
                while True:
                    booking_management_menu()
                    booking_choice = input("Select an option (1-3): ").strip()

                    if booking_choice == '1':
                        city_id = int(input("Enter the city ID where you want to book a cab: ").strip())
                        book_cab(booking_manager, city_id)

                    elif booking_choice == '2':
                        booking_id = int(input("Enter the booking ID to end the trip: ").strip())
                        end_trip(booking_manager, booking_id)

                    elif booking_choice == '3':
                        break

                    else:
                        logger.warning("Invalid option selected. Please try again.")

            elif choice == '4':
                show_analytics(cab_manager, city_manager)

            elif choice == '5':
                logger.info("Exiting the program.")
                break

            else:
                logger.warning("Invalid option selected. Please try again.")
    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()
