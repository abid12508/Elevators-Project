"""
BuildingState.py

Copyright 2026 University of Michigan EECS183

EECS 183 (Python): Final Project - Elevators
"""

from Utility import NUM_FLOORS, NUM_ELEVATORS, MAX_PEOPLE_PER_FLOOR

########################################################
######### DO NOT MODIFY ANY CODE IN THIS FILE ##########
########################################################

######################################################################
## BuildingState                                                    ##
## ----------------                                                 ##
## These classes will contain state information                     ##
## to be passed to the AI for further use                           ##
######################################################################

class PersonState:
    def __init__(self):
        """
        Requires: Nothing
        Modifies: anger_level
        Effects:  Initializes a PersonState object to store a person's
                  anger level, used for recording building state.
        """
        self.anger_level = 0


class FloorState:
    def __init__(self):
        """
        Requires: Nothing
        Modifies: floor_num, num_people, has_up_request,
                  has_down_request, people
        Effects:  Initializes a FloorState object to store information
                  about a floor, including floor number, number of people,
                  request flags, and a list of PersonState objects.
        """
        self.floor_num = 0
        self.num_people = 0
        self.has_up_request = False
        self.has_down_request = False
        self.people = [PersonState() for _ in range(MAX_PEOPLE_PER_FLOOR)]


class ElevatorState:
    def __init__(self):
        """
        Requires: Nothing
        Modifies: elevator_id, target_floor, current_floor,
                  is_servicing
        Effects:  Initializes an ElevatorState object to store information
                  about an elevator, including ID, target floor, current
                  floor, and servicing status.
        """
        self.elevator_id = 0
        self.target_floor = 0
        self.current_floor = 0
        self.is_servicing = False


class BuildingState:
    def __init__(self):
        """
        Requires: Nothing
        Modifies: turn, floors, elevators
        Effects:  Initializes a BuildingState object to store the complete
                  state of the building, including current turn, a list
                  of FloorState objects, and a list of ElevatorState
                  objects.
        """
        self.turn = 0
        self.floors = [FloorState() for _ in range(NUM_FLOORS)]
        self.elevators = [ElevatorState() for _ in range(NUM_ELEVATORS)]
