"""
State Manager Module
"""

from .state import State, IdleState, ReservedState, OnTripState

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
        elif stateName == "RESERVED":
            return ReservedState()
        elif stateName == "ON_TRIP":
            return OnTripState()
        else:
            raise ValueError(f"Unknown state: {stateName}")
