import unittest
from datetime import datetime
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.cab_management.utils import load_initial_data
    from src.cab_management.cab_manager import CabManager
    from src.cab_management.cab import CabState
except ImportError:
    sys.path.insert(0, 'src')
    from cab_management.utils import load_initial_data
    from cab_management.cab_manager import CabManager
    from cab_management.cab import CabState

class TestCabManager(unittest.TestCase):

    def setUp(self):
        """Set up initial data for testing."""
        load_initial_data()
        logger.info("Initial data loaded.")

        # Create an instance of CabManager
        self.cab_manager = CabManager.getInstance()
        logger.info("CabManager instance created.")

        self.cab_id = 101
        self.city_id = 1
        self.cab_manager.registerCab(self.cab_id, self.city_id)
        logger.info(f"Cab registered with ID: {self.cab_id} in city ID: {self.city_id}")

    def test_registerCab(self):
        """Test the registerCab method."""
        cab = self.cab_manager.getCab(self.cab_id)
        self.assertIsNotNone(cab, "Cab should not be None after registration")
        self.assertEqual(cab.cabId, self.cab_id, "Cab ID should match the registered cab ID")
        self.assertEqual(cab.cityId, self.city_id, "City ID should match the registered city ID")
        logger.info("registerCab test passed.")

    def test_updateCab(self):
        """Test the updateCab method."""
        new_state = CabState.RESERVED
        self.cab_manager.updateCab(self.cab_id, state=new_state)
        cab = self.cab_manager.getCab(self.cab_id)
        self.assertEqual(cab.getState(), new_state, "Cab state should be updated to RESERVED")
        logger.info("updateCab test passed.")

    def test_getCab(self):
        """Test the getCab method."""
        cab = self.cab_manager.getCab(self.cab_id)
        self.assertIsNotNone(cab, "Cab should not be None")
        self.assertEqual(cab.cabId, self.cab_id, "Cab ID should match the requested cab ID")
        logger.info("getCab test passed.")

    def test_getAllBookings(self):
        """Test the getAllBookings method."""
        all_bookings = self.cab_manager.getAllBookings()
        self.assertIsInstance(all_bookings, list, "getAllBookings should return a list")
        logger.info("getAllBookings test passed.")

if __name__ == '__main__':
    unittest.main()

