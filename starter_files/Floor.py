"""
Floor.py

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

from Person import Person
from Utility import MAX_PEOPLE_PER_FLOOR, MAX_ANGER, TICKS_PER_ANGER_INCREASE


class Floor:
    def __init__(self):
        # Do not modify this method
        self.people = []
        self.num_people = 0
        self.has_up_request = False
        self.has_down_request = False

    def reset_requests(self) -> None:
        """
        Requires: Nothing
        Modifies: has_up_request, has_down_request
        Effects: Search through people to find if there are any
                 pending up requests or down requests. Set the
                 values of has_up_request and has_down_request appropriately.
                 This function is used to recalculate requests whenever
                 the people on this floor are added or removed.
        """
        # TO DO
        pass

    def add_person(self, new_person: Person, request: int) -> None:
        """
        Requires: request != 0
        Modifies: has_up_request, has_down_request, num_people, people
        Effects:  If there is still room, add new_person to people.
                  Updates has_up_request or has_down_request based on value of
                  request
        """
        # TO DO
        pass

    def remove_people(
        self,
        indices_to_remove: list[int]
    ) -> None:
        """
        Requires: len(indices_to_remove) <= num_people,
                  for all values of i such that
                  0 <= i < len(indices_to_remove),
                  0 <= indices_to_remove[i] < num_people
        Modifies: people[], num_people, has_up_request, has_down_request
        Effects:  Removes objects from people[] at indices specified
                  in indices_to_remove[].
                  After removals, calls reset_requests() to update
                  has_up_request and has_down_request.
        """
        # TO DO
        pass

    def tick(self, current_time: int) -> int:
        """
        Requires: Nothing
        Modifies: people
        Effects:  Ticks each person on this floor
                  Also removes any Person who explodes
                  Returns the number of exploded people
        """
        # TO DO
        return -1

    ######################################################
    ###### DO NOT MODIFY ANY CODE BENEATH THIS LINE ######
    ######################################################

    def get_person_by_index(self, index: int) -> Person:
        """
        Requires: 0 <= index < num_people
        Modifies: Nothing
        Effects:  Returns the person at given index of people list
        """
        return self.people[index]

    def get_num_people(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns the number of people on this floor
        """
        return self.num_people

    def set_has_up_request(self, has_request: bool) -> None:
        """
        Requires: Nothing
        Modifies: has_up_request
        Effects:  Sets has_up_request to the given value
        """
        self.has_up_request = has_request

    def get_has_up_request(self) -> bool:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns whether this floor has an up_request
        """
        return self.has_up_request

    def set_has_down_request(self, has_request: bool) -> None:
        """
        Requires: Nothing
        Modifies: has_down_request
        Effects:  Sets has_down_request to the given value
        """
        self.has_down_request = has_request

    def get_has_down_request(self) -> bool:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns whether this floor has a down_request
        """
        return self.has_down_request

    def print_floor_pickup_menu(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Prints the pickup menu of this floor
        """
        print("\nSelect People to Load by Index")
        print("All people must be going in same direction!")

        heads = " ".join([" O  " for _ in range(self.num_people)])
        print("              " + heads)
        torsos = " ".join(["-|- " for _ in range(self.num_people)])
        print("              " + torsos)
        arms = " ".join([" |  " for _ in range(self.num_people)])
        print("              " + arms)
        legs = " ".join(["/ \\ " for _ in range(self.num_people)])
        print("              " + legs)

        indices = " ".join([f" {i}  " for i in range(
            self.num_people
        )])
        print("INDEX:        " + indices)
        anger = " ".join([f" {p.get_anger_level()}  " for p in
                          self.people])
        print("ANGER:        " + anger)
        targets = " ".join([f" {p.get_target_floor()}  " for p in
                           self.people])
        print("TARGET FLOOR: " + targets, end=' ')

    def pretty_print_floor_line1(self) -> None:
        line = ("U" if self.has_up_request else " ") + " "
        for p in self.people:
            line += str(p.get_anger_level())
            if p.get_anger_level() < MAX_ANGER:
                line += "   "
            else:
                line += "  "
        print(line)

    def pretty_print_floor_line2(self) -> None:
        line = ("D" if self.has_down_request else " ") + " "
        for _ in self.people:
            line += "o   "
        print(line)
