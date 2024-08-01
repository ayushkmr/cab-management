import unittest
from datetime import datetime
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.cab_management.utils import load_initial_data, add_booking
    from src.cab_management.booking import BookingState
    from src.cab_management.booking_manager import BookingManager
except ImportError:
    sys.path.insert(0, 'src')
    from cab_management.utils import load_initial_data, add_booking
    from cab_management.booking import BookingState
    from cab_management.booking_manager import BookingManager

class TestBooking(unittest.TestCase):

    def setUp(self):
        """Set up initial data for testing."""
        load_initial_data()  # Load initial data for consistent test environment
        logger.info("Initial data loaded for booking tests.")
        
        # Create an instance of BookingManager
        self.booking_manager = BookingManager.getInstance()
        
        # Create a booking for testing
        self.city_id = 1
        self.start_time = datetime(2024, 7, 25, 10, 0)  # Static start time for testing
        self.booking_id = add_booking(self.city_id, self.start_time)
        self.booking = self.booking_manager.bookings[self.booking_id]
        self.cab = self.booking.getCab()  # Assuming this retrieves the cab associated with the booking

    def test_initial_state(self):
        """Test the initial state of the booking."""
        self.assertEqual(self.booking.getState(), BookingState.TRIP_STARTED)
        self.assertEqual(self.booking.getCab(), self.cab, "Cab should match the booked cab")
        self.assertEqual(self.booking.getCity().cityId, self.city_id, "City ID should match the booked city ID")
        logger.info("test_initial_state passed.")

    def test_change_state(self):
        """Test the change_state method."""
        self.booking.change_state(BookingState.TRIP_STARTED)
        self.assertEqual(self.booking.getState(), BookingState.TRIP_STARTED, "Booking state should be updated to TRIP_STARTED")
        logger.info("test_change_state passed.")

    def test_get_start_time(self):
        """Test the getStartTime method."""
        self.assertEqual(self.booking.getStartTime(), self.start_time, "Start time should match the booking start time")
        logger.info("test_get_start_time passed.")

if __name__ == '__main__':
    unittest.main()
