"""
Elevator.py

Copyright 2026 University of Michigan EECS183

<#Name 1#>
<#Uniqname 1#>

<#Name 2#>
<#Uniqname 2#>

<#Name 3#>
<#Uniqname 3#>

<#Name 4#>
<#Uniqname 4#>

EECS 183 (Python): Final Project - Elevators
"""

from Utility import TICKS_PER_ELEVATOR_MOVE

class Elevator:
    def __init__(self):
        """
        Requires: Nothing
        Modifies: self
        Effects:  Creates an Elevator object with initial values

        Do not modify this method
        """
        self.servicing = False
        self.current_floor = 0
        self.target_floor = 0

    def tick(self, current_time: int) -> None:
        """
        Requires: current_time is valid
        Modifies: current_floor, servicing
        Effects:  If the current_time is divisible by TICKS_PER_ELEVATOR_MOVE
                  and the elevator is servicing a request:
                      Moves the value of current floor by 1 in the direction
                      of the target floor
                      Also, If the new current floor is the target floor:
                          servicing is set to false

                  Otherwise, does nothing
        """
        # TO DO
        pass

    def service_request(self, floor_num: int) -> None:
        """
        Requires: 0 <= floor_num < NUM_FLOORS
        Modifies: target_floor, servicing
        Effects:  Sets the target_floor and marks the Elevator as
                  currently servicing
        """
        # TO DO
        pass

    ######################################################
    ###### DO NOT MODIFY ANY CODE BENEATH THIS LINE ######
    ######################################################

    def print(self) -> None:
        """
        Requires: Nothing
        Modifies: print
        Effects:  Prints the info string of the elevator
        """
        print(self)

    def set_current_floor(self, current_floor_in: int) -> None:
        """
        Requires: 0 <= current_floor_in < NUM_FLOORS
        Modifies: current_floor
        Effects:  Sets the current_floor
        """
        self.current_floor = current_floor_in

    def is_servicing(self) -> bool:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns whether the elevator is servicing
        """
        return self.servicing

    def get_current_floor(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns the current_floor
        """
        return self.current_floor

    def get_target_floor(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns the target_floor
        """
        return self.target_floor

    def __str__(self) -> str:
        if not self.servicing:
            return f"{self.current_floor}w"
        return f"{self.current_floor}s{self.target_floor}"
