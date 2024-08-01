import unittest
import sys
from datetime import datetime, timedelta

# Add the src directory to the system path
try:
    from src.cab_management.analytics import Analytics
    from src.cab_management.utils import load_initial_data
    from src.cab_management.booking_manager import BookingManager
    from src.cab_management.cab_manager import CabManager
except ImportError:
    import sys
    sys.path.insert(0, 'src')
    from cab_management.analytics import Analytics
    from cab_management.utils import load_initial_data
    from cab_management.booking_manager import BookingManager
    from cab_management.cab_manager import CabManager


class TestAnalytics(unittest.TestCase):

    def setUp(self):
        """Set up initial data for testing."""
        load_initial_data()

        # Create instances of BookingManager and CabManager
        self.booking_manager = BookingManager.getInstance()
        self.cab_manager = CabManager.getInstance()

        self.cabId = 102
        self.cab = self.cab_manager.getCab(self.cabId)
        self.starttime = datetime(2024, 7, 25, 12, 0) - timedelta(hours=2) # Static start time for testing
        self.endtime = self.starttime + timedelta(hours=1)
        self.bookingId = self.booking_manager.bookCab(1, self.starttime)
        self.booking_manager.endBooking(self.bookingId, self.endtime)

    def test_calculateIdleTime(self):
        """Test the calculateIdleTime method."""
        self.booking = self.booking_manager.bookings[self.bookingId]
        idle_time = Analytics.calculateIdleTime(self.booking.getCab(), self.starttime, self.starttime + timedelta(hours=2))
        self.assertEqual(idle_time, 3600)

    def test_getCabHistory(self):
        """Test the getCabHistory method."""
        history, bookings = Analytics.getCabHistory(self.cab)
        self.assertGreater(len(history), 1)
        self.assertEqual(len(bookings), 1)

    def test_highDemandCities(self):
        """Test the highDemandCities method."""
        high_demand_city, peak_time = Analytics.highDemandCities(self.booking_manager.getAllBookings())
        self.assertEqual(high_demand_city, 'New York')
        self.assertEqual(peak_time, 10)  # Peak hour is 10 AM

if __name__ == '__main__':
    unittest.main()
