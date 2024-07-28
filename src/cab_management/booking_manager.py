"""
Booking Manager Module
"""

import logging
from datetime import datetime

class BookingManager:
    """
    Manages the booking of cabs.
    """

    @staticmethod
    def findBestCab(cabs, city):
        """
        Find the best available cab in the given city.
        
        Args:
            cabs (dict): Dictionary of cabs.
            city (str): The city where the cab is needed.
        
        Returns:
            Cab: The best available cab object, or None if no cabs are available.
        """
        idleCabs = [cab for cab in cabs.values() if cab.getLocation() == city and cab.getState().__class__.__name__ == "IdleState"]
        if not idleCabs:
            logging.warning(f"No idle cabs available in city {city}")
            return None
        idleCabs.sort(key=lambda cab: sum(1 for time, state in cab.getHistory() if state.__class__.__name__ == "IdleState"), reverse=True)
        selected_cab = idleCabs[0] if idleCabs else None
        if selected_cab:
            selected_cab.setState("ON_TRIP")
            logging.info(f"Selected cab {selected_cab.cabId} for booking in city {city}")
        return selected_cab
