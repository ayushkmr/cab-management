"""
Analytics Module
"""

from collections import defaultdict
from datetime import timedelta

class Analytics:
    """
    Provides analytics for the cab management system.
    """

    @staticmethod
    def calculateIdleTime(cab, startTime, endTime):
        """
        Calculate the total idle time of a cab in the given duration.
        
        Args:
            cab (Cab): The cab object.
            startTime (datetime): The start time of the period.
            endTime (datetime): The end time of the period.
        
        Returns:
            timedelta: The total idle time.
        """
        idleTime = timedelta(0)
        previous_time = None
        for time, state in cab.getHistory():
            if previous_time is None:
                previous_time = time
                continue
            if state.__class__.__name__ == "IdleState":
                if (startTime is None or time >= startTime) and (endTime is None or time <= endTime):
                    idleTime += time - previous_time
            previous_time = time
        return idleTime

    @staticmethod
    def getCabHistory(cab):
        """
        Get the history of states a cab has gone through.
        
        Args:
            cab (Cab): The cab object.
        
        Returns:
            list: The history of states with timestamps.
        """
        return cab.getHistory()

    @staticmethod
    def highDemandCities(bookings):
        """
        Find cities with the highest demand for cabs and the time when the demand is highest.
        
        Args:
            bookings (list): List of Booking objects.
        
        Returns:
            tuple: The city with the highest demand and the peak time of demand.
        """
        demand = defaultdict(int)
        demand_times = defaultdict(list)
        for booking in bookings:
            demand[booking.city.cityId] += 1
            demand_times[booking.city.cityId].append(booking.time)
        sorted_demand = sorted(demand.items(), key=lambda item: item[1], reverse=True)
        high_demand_city = sorted_demand[0][0] if sorted_demand else None
        peak_time = None
        if high_demand_city:
            times = demand_times[high_demand_city]
            peak_time = max(set(times), key=times.count)
        return high_demand_city, peak_time
