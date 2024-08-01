"""
City Module
"""

class City:
    """
    Represents a City.
    
    Attributes:
        cityId (int): Unique identifier for the city.
        name (str): Name of the city.
        cabs (dict): Dictionary mapping cab IDs to Cab objects.
    """
    def __init__(self, cityId, name):
        self.cityId = cityId
        self.name = name
        self.cabs = {}  # cabId -> Cab object

    def addCab(self, cab):
        """
        Add a cab to the city.
        
        Args:
            cab (Cab): The cab object to be added.
        """
        self.cabs[cab.cabId] = cab

    def removeCab(self, cabId):
        """
        Remove a cab from the city.
        
        Args:
            cabId (int): The cab ID to be removed.
        """
        if cabId in self.cabs:
            del self.cabs[cabId]

    def getCabs(self):
        """
        Get all cabs in the city.
        
        Returns:
            list: List of cab objects.
        """
        return list(self.cabs.values())

    def getCabsByState(self, state):
        """
        Get all cabs in the city with a given state.
        
        Args:
            state (CabState): The state to filter cabs by.
        
        Returns:
            list: List of cab objects with the given state.
        """
        return [cab for cab in self.cabs.values() if cab.getState() == state]
