import unittest
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.cab_management.cab import Cab, CabState
    from src.cab_management.cab_manager import CabManager
except ImportError:
    sys.path.insert(0, 'src')
    from cab_management.cab import Cab, CabState
    from cab_management.cab_manager import CabManager

class TestCab(unittest.TestCase):

    def setUp(self):
        """Set up initial data for testing."""
        self.cab_manager = CabManager.getInstance()
        self.cab_id = 102
        self.city_id = 1
        self.cab_manager.registerCab(self.cab_id, self.city_id)
        self.cab = self.cab_manager.getCab(self.cab_id)
        logger.info(f"Cab registered with ID: {self.cab_id} in city ID: {self.city_id}")

    def test_initial_state(self):
        """Test the initial state of the cab."""
        self.assertEqual(self.cab.getState().name, "IDLE", "Initial state should be IDLE")
        self.assertEqual(self.cab.getCity(), self.city_id, "City ID should match the registered city ID")
        logger.info("test_initial_state passed.")

    def test_set_state(self):
        """Test the setState method."""
        self.cab.setState(CabState.RESERVED)
        self.assertEqual(self.cab.getState(), CabState.RESERVED, "Cab state should be updated to RESERVED")
        logger.info("test_set_state passed.")

    def test_get_history(self):
        """Test the getHistory method."""
        history = self.cab.getHistory()
        self.assertIsInstance(history, list, "History should be a list")
        self.assertGreater(len(history), 0, "History should not be empty")
        logger.info("test_get_history passed.")

if __name__ == '__main__':
    unittest.main()
