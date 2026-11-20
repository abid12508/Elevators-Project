"""
Move.py

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

from Utility import NUM_ELEVATORS, NUM_FLOORS, MAX_PEOPLE_PER_FLOOR, MAX_ANGER
from Elevator import Elevator
from Floor import Floor
from Person import Person


class Move:
    def __init__(self, command_string: str = ""):
        """
        Requires: command_string is a valid string
        Modifies: elevator_id, target_floor, is_pass, is_pickup, is_save,
                  is_quit
        Effects:  creates a Move object based on
                  the characters in command_string

                  Examples:
                  command_string = "e1f4"
                  - elevator_id of 1 has a target_floor of 4
                  command_string = "e1p"
                  - elevator_id of 1 will pickup people on its current floor

                  when command_string is "", or "S", or "Q", etc.:
                       sets the corresponding attribute to true
        """
        # TO DO
        pass

    def is_valid_move(self, elevators: list[Elevator]) -> bool:
        """
        Requires: elevators represents the elevator servicing states
        Modifies: Nothing
        Effects:  returns true if this Move instance is valid, false otherwise

                  The following are the criterion for validity:

                  If a move is a Pass Move, a Quit Move, or a Save Move
                  it is valid.
                  For both Pickup Moves and Servicing Moves:
                      0 <= elevator_id < NUM_ELEVATORS
                      The corresponding Elevator is currently not
                         servicing a request.
                  For Servicing Moves only:
                      0 <= target_floor < NUM_FLOORS
                      target_floor is different from the corresponding
                         Elevator's current_floor
        """
        # TO DO
        return False

    def set_people_to_pickup(self, pickup_list: str, current_floor: int,
                             pickup_floor: Floor) -> None:
        """
        Requires: pickup_list is a valid list of indices
                  current_floor is the floor number where the pickup
                    is taking place
                  pickup_floor is the Floor instance where the pickup
                   is taking place
        Modifies: num_people_to_pickup, people_to_pickup, total_satisfaction,
                  target_floor
        Effects:  sets num_people_to_pickup and total_satisfaction to 0
                  adds the indices specified in pickup_list to people_to_pickup
                  increments num_people_to_pickup by 1 for each person being
                  picked up
                  adds satisfaction gained from each person picked up
                     to total_satisfaction
                  sets target_floor to be the most extreme floor of those
                     being picked up (furthest up or down)
        """
        # TO DO
        pass

    ######################################################
    ###### DO NOT MODIFY ANY CODE BENEATH THIS LINE ######
    ######################################################

    def is_pickup_move(self) -> bool:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns the value of is_pickup
        """
        return self.is_pickup

    def is_pass_move(self) -> bool:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns the value of is_pass
        """
        return self.is_pass

    def is_save_move(self) -> bool:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns the value of is_save
        """
        return self.is_save

    def is_quit_move(self) -> bool:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns the value of is_quit
        """
        return self.is_quit

    def get_elevator_id(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns the elevator_id
        """
        return self.elevator_id

    def get_target_floor(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns the target_floor
        """
        return self.target_floor

    def get_num_people_to_pickup(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns the number of people being picked up by
                 this move (0 if not a pickup move)
        """
        return self.num_people_to_pickup

    def get_total_satisfaction(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns total_satisfaction
        """
        return self.total_satisfaction

    def set_target_floor(self, in_target_floor: int) -> None:
        """
        Requires: in_target_floor is a valid floor
        Modifies: target_floor
        Effects: sets the target_floor to in_target_floor
        """
        self.target_floor = in_target_floor

    def copy_list_of_people_to_pickup(self) -> list[int]:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: returns a copy of the list of people to pick up
        """
        return self.people_to_pickup[:self.num_people_to_pickup]
