"""
State Manager Module
"""

class State:
    """Base class for all states"""
    pass

class IdleState(State):
    """Represents the idle state"""
    pass

class OnTripState(State):
    """Represents the on-trip state"""
    pass

class StateManager:
    """
    Manages the states of cabs.
    """

    @staticmethod
    def getState(stateName):
        """
        Get the state object for the given state name.
        
        Args:
            stateName (str): The name of the state.
        
        Returns:
            State: The state object.
        """
        if stateName == "IDLE":
            return IdleState()
        elif stateName == "ON_TRIP":
            return OnTripState()
        else:
            raise ValueError(f"Unknown state: {stateName}")
