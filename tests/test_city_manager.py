import unittest
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from src.cab_management.city_manager import CityManager
except ImportError:
    sys.path.insert(0, 'src')
    from cab_management.city_manager import CityManager

class TestCityManager(unittest.TestCase):

    def setUp(self):
        """Set up initial data for testing."""
        self.city_manager = CityManager.getInstance()
        self.city_id = 1
        self.city_name = "New York"
        self.city_manager.addCity(self.city_id, self.city_name)
        logger.info(f"City added with ID: {self.city_id} and Name: {self.city_name}")

    def test_addCity(self):
        """Test the addCity method."""
        city = self.city_manager.getCity(self.city_id)
        self.assertIsNotNone(city, "City should not be None after addition")
        self.assertEqual(city.name, self.city_name, "City name should match the added city name")
        logger.info("addCity test passed.")

    def test_getCity(self):
        """Test the getCity method."""
        city = self.city_manager.getCity(self.city_id)
        self.assertIsNotNone(city, "City should not be None")
        self.assertEqual(city.cityId, self.city_id, "City ID should match the requested city ID")
        logger.info("getCity test passed.")

    def test_removeCity(self):
        """Test the removeCity method."""
        result = self.city_manager.removeCity(self.city_id)
        self.assertTrue(result, "City should be removed successfully")
        self.assertIsNone(self.city_manager.getCity(self.city_id), "City should be None after removal")
        logger.info("removeCity test passed.")

    def test_getAllCities(self):
        """Test the getAllCities method."""
        all_cities = self.city_manager.getAllCities()
        self.assertIn(self.city_manager.getCity(self.city_id), all_cities, "All cities should include the added city")
        logger.info("getAllCities test passed.")

if __name__ == '__main__':
    unittest.main()
