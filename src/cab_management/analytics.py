"""
Analytics Module
"""

from datetime import datetime, timedelta
import logging
from .cab import Cab, CabState

logger = logging.getLogger('cab_management.analytics')

class Analytics:
    """
    Provides analytical methods for cab management.
    """

    @staticmethod
    def calculateIdleTime(cab, start_time, end_time):
        """
        Calculate the total idle time of a cab between start_time and end_time.
        
        Args:
            cab (Cab): The cab whose idle time is to be calculated.
            start_time (datetime): The start time of the period to calculate idle time.
            end_time (datetime): The end time of the period to calculate idle time.
        
        Returns:
            float: The total idle time in hours.
        """
        if start_time is None:
            start_time = datetime.min
            logger.warning("Start time is None, setting it to datetime.min")
        if end_time is None:
            end_time = datetime.now()
            logger.warning("End time is None, setting it to datetime.now()")

        total_idle_time = timedelta(0)
        current_time = datetime.now()
        previous_time = start_time

        logger.debug(f"Calculating idle time for cab {cab.cabId}")
        for time, state in cab.getHistory():
            if state == CabState.IDLE:
                if previous_time < time <= end_time:
                    total_idle_time += time - previous_time
                previous_time = time
        
        if previous_time < end_time and cab.getState() == CabState.IDLE:
            total_idle_time += end_time - previous_time
        
        idle_time_hours = total_idle_time.total_seconds() / 3600.0
        logger.info(f"Calculated idle time for cab {cab.cabId}: {idle_time_hours} hours")
        return idle_time_hours

    @staticmethod
    def getCabHistory(cab):
        """
        Get the history of states for a cab and its bookings.
        
        Args:
            cab (Cab): The cab whose history is to be retrieved.
        
        Returns:
            tuple: The history of states for the cab and the list of bookings.
        """
        history = cab.getHistory()
        bookings = cab.getBookings()
        logger.info(f"Retrieved history for cab {cab.cabId}: {history}")
        logger.info(f"Bookings for cab {cab.cabId}: {bookings}")
        return history, bookings

    @staticmethod
    def highDemandCities(bookings):
        """
        Find the city with the highest demand for cabs and the peak time.
        
        Args:
            bookings (list): List of all bookings.
        
        Returns:
            tuple: City with the highest demand and the peak time.
        """
        city_demand = {}
        time_demand = {}

        for booking in bookings:
            city = booking.city
            booking_time = datetime.fromisoformat(booking.start_time).hour

            if city not in city_demand:
                city_demand[city] = 0
            city_demand[city] += 1

            if booking_time not in time_demand:
                time_demand[booking_time] = 0
            time_demand[booking_time] += 1

        high_demand_city = max(city_demand, key=city_demand.get)
        peak_time = max(time_demand, key=time_demand.get)

        logger.info(f"High demand city: {high_demand_city}, Peak time: {peak_time}")
        return high_demand_city, peak_time
