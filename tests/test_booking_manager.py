import unittest
from datetime import datetime
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.cab_management.utils import load_initial_data
    from src.cab_management.booking_manager import BookingManager
    from src.cab_management.booking import BookingState
except ImportError:
    sys.path.insert(0, 'src')
    from cab_management.utils import load_initial_data
    from cab_management.booking_manager import BookingManager
    from cab_management.booking import BookingState

class TestBookingManager(unittest.TestCase):

    def setUp(self):
        """Set up initial data for testing."""
        load_initial_data()
        logger.info("Initial data loaded.")

        # Create an instance of BookingManager
        self.booking_manager = BookingManager.getInstance()
        logger.info("BookingManager instance created.")

        self.city_id = 1
        self.start_time = datetime(2024, 7, 25, 10, 0)  # Static start time for testing
        self.booking_id = self.booking_manager.bookCab(self.city_id, self.start_time)
        logger.info(f"Booking created with ID: {self.booking_id} for city ID: {self.city_id} at {self.start_time}")

    def test_bookCab(self):
        """Test the bookCab method."""
        self.assertIsNotNone(self.booking_id, "Booking ID should not be None")
        booking = self.booking_manager.bookings[self.booking_id]
        self.assertEqual(booking.city.cityId, self.city_id, "City ID should match the booking city")
        self.assertEqual(booking.start_time, self.start_time, "Start time should match the booking start time")
        logger.info("bookCab test passed.")

    def test_endBooking(self):
        """Test the endBooking method."""
        end_time = datetime(2024, 7, 25, 11, 0)  # Static end time for testing
        self.booking_manager.endBooking(self.booking_id, end_time)
        booking = self.booking_manager.bookings[self.booking_id]
        self.assertEqual(booking.getState(), BookingState.COMPLETED, "Booking state should be COMPLETED")
        self.assertEqual(booking.getEndTime(), end_time, "End time should match the provided end time")
        logger.info("endBooking test passed.")

    def test_getAllBookings(self):
        """Test the getAllBookings method."""
        all_bookings = self.booking_manager.getAllBookings()
        self.assertIn(self.booking_manager.bookings[self.booking_id], all_bookings, "All bookings should include the created booking")
        logger.info("getAllBookings test passed.")

if __name__ == '__main__':
    unittest.main()

