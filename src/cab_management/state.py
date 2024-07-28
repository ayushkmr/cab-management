"""
State Module
"""

class State:
    """
    Base class for cab states.
    """
    def changeState(self, cab, state):
        pass

class IdleState(State):
    """
    State representing an idle cab.
    """
    def changeState(self, cab, state):
        if state == "ON_TRIP":
            cab.setState("ON_TRIP")

class OnTripState(State):
    """
    State representing a cab that is on a trip.
    """
    def changeState(self, cab, state):
        if state == "IDLE":
            cab.setState("IDLE")
