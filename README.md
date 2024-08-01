# Cab Management System

## Overview
The Cab Management System is a comprehensive solution designed to manage cabs, bookings, and cities efficiently. This system includes functionalities to register and update cabs, handle bookings, manage city data, and perform various analytics. The system is implemented in Python and leverages a modular structure to ensure clean, maintainable, and extensible code.

## Features
### Cab Management:
- **Register new cabs:** Easily register new cabs with unique IDs and assign them to cities.
- **Update existing cabs' state and city:** Change the state (e.g., IDLE, ON_TRIP) of a cab and reassign it to different cities.
- **View booking history of cabs:** Access the complete booking history of individual cabs.
- **View state change history of cabs:** Track the state changes of cabs over time.

### Booking Management:
- **Book a cab in a specified city:** Reserve a cab for a trip within a specific city.
- **End a trip and make the cab available:** Conclude a trip and make the cab available for future bookings.

### City Management:
- **Add new cities:** Introduce new cities into the system where cabs can be registered and operate.
- **View all cabs in a city:** List all the cabs currently available in a specified city.
- **View cabs in a city by their state:** Filter and view cabs based on their state (e.g., IDLE, ON_TRIP) within a city.
- **Remove cities:** Remove cities from the system, provided they do not have any associated cabs.

### Analytics:
- **Calculate total idle time of a cab in a given duration:** Compute the total idle time for a cab within a specified time range.
- **View the state change history of cabs:** Access the history of state changes for individual cabs.
- **Identify cities with the highest demand for cabs and peak times:** Analyze and determine high-demand cities and peak booking times.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd cab-management
   ```
3. Install the required dependencies (if any). You can use a package manager like `pip` to install dependencies listed in a `requirements.txt` file, if available:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the main application:
   ```bash
   python src/cab_management/main.py
   ```
2. Follow the on-screen menu to navigate through the various functionalities. The menu will provide options for cab management, booking management, city management, and analytics.
3. To load initial data, select the option to load data from a JSON file. Ensure that the file structure matches the expected format for cities, cabs, and bookings.

## Data Management
- **Initial Data Loading:** Initial data can be loaded from a JSON file. Ensure the file structure matches the expected format for cities, cabs, and bookings. The application will prompt you to enter the path to the JSON file when you choose to load initial data.

## Additional Notes
- Make sure to have Python installed on your machine. The application is compatible with Python 3.x.
- For any issues or contributions, please refer to the project's issue tracker on the repository.

---

## Directory Structure
```
cab-management/
│
├── data/
│   ├── initial_data.json
│   └── input.json
│
├── src/
│   ├── cab_management/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── booking_manager.py
│   │   ├── booking.py
│   │   ├── cab_manager.py
│   │   ├── cab.py
│   │   ├── city_manager.py
│   │   ├── city.py
│   │   ├── utils.py
│   │   └── main.py
│
├── tests/
│   ├── __init__.py
│   ├── test_analytics.py
│   ├── test_booking_manager.py
│   ├── test_booking.py
│   ├── test_cab_manager.py
│   ├── test_cab.py
│   ├── test_city_manager.py
│   ├── test_city.py
│   └── test_utils.py
│
├── .gitignore
└── README.md
```

## Module Descriptions

### `src/cab_management/main.py`
The main entry point for running the cab management portal. It initializes the managers and provides a user interface for interacting with the system.

### `src/cab_management/cab.py`
Defines the `Cab` class which represents a cab and handles its state, city, booking history, and state change history.

### `src/cab_management/cab_manager.py`
Manages the operations related to cabs, including registration, updates, and fetching cabs.

### `src/cab_management/city_manager.py`
Manages city-related operations, including adding, removing, and fetching cabs by city.

### `src/cab_management/booking_manager.py`
Handles booking-related operations, including creating and ending bookings.

### `src/cab_management/analytics.py`
Provides analytical functions such as calculating idle times, tracking state changes, and identifying high-demand cities.

### `src/cab_management/utils.py`
Utility functions for tasks such as loading initial data from JSON files.

---

## Example Usage
1. **Register a Cab:**
   - Register a cab with ID 101 in city with ID 1:
     ```bash
     python src/cab_management/main.py
     ```
   - Choose the cab management menu, then choose to register a cab. Enter 101 as the cab ID and 1 as the city ID.

2. **Book a Cab:**
   - Book a cab in city with ID 1:
     ```bash
     python src/cab_management/main.py
     ```
   - Choose the booking management menu, then choose to book a cab. Enter 1 as the city ID.

3. **View Analytics:**
   - View cab idle time:
     ```bash
     python src/cab_management/main.py
     ```
   - Choose the analytics menu, then choose to show cab idle time. Enter the cab ID and the time range.


## Contributions
Contributions are welcome! Please create a pull request with a detailed description of your changes.

For any issues, please open an issue on the project's GitHub repository.