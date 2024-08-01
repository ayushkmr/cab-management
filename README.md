# cab-management
An inter-city cab management portal designed for efficient cab administration and booking management. This tool allows users to:

## Features
- **Cab Registration**: Easily register new cabs in specified cities.
- **Cab State Management**: Update the state of cabs (e.g., IDLE, ON_TRIP) and track their history.
- **Booking Management**: Book cabs in various cities, view booking history, and end trips.
- **City Management**: Add, remove, and manage cities where cabs operate.
- **Analytics**: Access analytics on cab usage, idle times, and high-demand cities.

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
   python src/main.py
   ```
2. Follow the on-screen menu to navigate through the various functionalities. The menu will provide options for cab management, booking management, city management, and analytics.
3. To load initial data, select the option to load data from a JSON file. Ensure that the file structure matches the expected format for cities, cabs, and bookings.

## Data Management
- Initial data can be loaded from a JSON file. Ensure the file structure matches the expected format for cities, cabs, and bookings. The application will prompt you to enter the path to the JSON file when you choose to load initial data.

## Additional Notes
- Make sure to have Python installed on your machine. The application is compatible with Python 3.x.
- For any issues or contributions, please refer to the project's issue tracker on the repository.
