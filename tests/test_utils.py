import unittest
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.cab_management.utils import load_initial_data, add_booking, end_trip_with_timestamp
    from src.cab_management.booking_manager import BookingManager
    from src.cab_management.booking import BookingState
except ImportError:
    sys.path.insert(0, 'src')
    from cab_management.utils import load_initial_data, add_booking, end_trip_with_timestamp
    from cab_management.booking_manager import BookingManager
    from cab_management.booking import BookingState

class TestUtils(unittest.TestCase):

    def setUp(self):
        """Set up initial data for testing."""
        load_initial_data()
        logger.info("Initial data loaded for utils tests.")

    def test_add_booking(self):
        """Test the add_booking function."""
        city_id = 2
        booking_id = add_booking(city_id)
        self.assertIsNotNone(booking_id, "Booking ID should not be None after adding a booking")
        logger.info(f"Booking {booking_id} added for city ID: {city_id}")

    def test_end_trip_with_timestamp(self):
        """Test the end_trip_with_timestamp function."""
        city_id = 15
        booking_id = add_booking(city_id)
        result = end_trip_with_timestamp(booking_id)
        self.assertTrue(result, "Ending the trip should return True")
        # Assuming we can check the state of the booking after ending the trip
        bookings = BookingManager.getInstance().getBookings()
        booking = bookings[booking_id]
        self.assertEqual(booking.state, BookingState.COMPLETED, "Booking should be completed after ending the trip")
        logger.info(f"Trip for booking ID {booking_id} ended successfully.")

if __name__ == '__main__':
    unittest.main()
