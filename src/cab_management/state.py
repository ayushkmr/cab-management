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
        if state == "RESERVED":
            cab.setState("RESERVED")

class ReservedState(State):
    """
    State representing a reserved cab.
    
    The reserved state is added to indicate that a cab has been booked and is waiting for the customer to start the trip.
    This state helps in managing the cab's availability more accurately by distinguishing between a cab that is simply idle
    and one that is reserved but not yet on a trip.
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
