
import unittest
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.cab_management.city import City
    from src.cab_management.cab import Cab
except ImportError:
    sys.path.insert(0, 'src')
    from cab_management.city import City
    from cab_management.cab import Cab

class TestCity(unittest.TestCase):

    def setUp(self):
        """Set up initial data for testing."""
        self.city_id = 1
        self.city_name = "New York"
        self.city = City(self.city_id, self.city_name)
        logger.info(f"City created with ID: {self.city_id} and Name: {self.city_name}")

    def test_initial_attributes(self):
        """Test the initial attributes of the city."""
        self.assertEqual(self.city.cityId, self.city_id, "City ID should match the initialized city ID")
        self.assertEqual(self.city.name, self.city_name, "City name should match the initialized city name")
        self.assertEqual(self.city.getCabs(), [], "Initial cabs list should be empty")
        logger.info("test_initial_attributes passed.")

    def test_add_cab(self):
        """Test the addCab method."""
        cab_id = 101
        self.city.addCab(Cab(cab_id, self.city_id))  # Assuming Cab class has been defined
        self.assertIn(cab_id, self.city.cabs, "Cab should be added to the city's cabs")
        logger.info("test_add_cab passed.")

    def test_remove_cab(self):
        """Test the removeCab method."""
        cab_id = 101
        self.city.addCab(Cab(cab_id, self.city_id))  # Add cab first
        self.city.removeCab(cab_id)
        self.assertNotIn(cab_id, self.city.cabs, "Cab should be removed from the city's cabs")
        logger.info("test_remove_cab passed.")

    def test_get_cabs(self):
        """Test the getCabs method."""
        cab_id = 101
        self.city.addCab(Cab(cab_id, self.city_id))  # Add cab first
        cabs = self.city.getCabs()
        self.assertEqual(len(cabs), 1, "There should be one cab in the city")
        self.assertEqual(cabs[0].cabId, cab_id, "The cab ID should match the added cab ID")
        logger.info("test_get_cabs passed.")

if __name__ == '__main__':
    unittest.main()
