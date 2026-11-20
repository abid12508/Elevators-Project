"""
Person.py

Copyright 2026 University of Michigan EECS183

Evan Roetman
evancr

<#Name 2#>
<#Uniqname 2#>

<#Name 3#>
<#Uniqname 3#>

<#Name 4#>
<#Uniqname 4#>

EECS 183 (Python): Final Project - Elevators
"""

from Utility import TICKS_PER_ANGER_INCREASE, MAX_ANGER


class Person:
    def __init__(self, input_string: str | None = None):
        """
        Requires: input_string is correctly formatted
        Modifies: turn, current_floor, target_floor,
                  anger_level
        Effects:  Parses input_string to set attributes
                  An example of input_string is "7f4t8a3".
        """
        if input_string == None:
            self.turn = 0
            self.anger_level = 0
            self.current_floor = 0
            self.target_floor = 0
        else:
            # Create list of form:
            # info = [tick, current_floor, target_floor, anger_level]
            info = []
            num = ''
            for char in input_string:
                if char.isnumeric():
                    num += char
                else:
                    info.append(int(num))
                    num = ''
            info.append(int(num))

            # Assign list items to attributes
            self.turn = int(info[0])
            self.current_floor = int(info[1])
            self.target_floor = int(info[2])
            self.anger_level = int(info[3])

    def tick(self, current_time: int) -> bool:
        """
        Requires: Nothing
        Modifies: anger_level
        Effects:  Every TICKS_PER_ANGER_INCREASE, this function
                  increases the person's anger level by 1. If,
                  after increasing, the person has an anger level
                  of MAX_ANGER, the function will return true. If
                  the person has an anger level less than MAX_ANGER,
                  the function will return false.
        """
        if current_time % TICKS_PER_ANGER_INCREASE == 0:
            self.anger_level += 1
        return self.anger_level >= MAX_ANGER

    def print(self) -> None:
        """
        Requires: Nothing
        Modifies: print
        Effects:  Prints the info_string of the person NOT
                  including the turn

        Examples: p = Person('7f4t8a3')
                  p.print()

                  This will print 'f4t8a3' to the screen
        """
        print(self.__str__())

    ######################################################
    ###### DO NOT MODIFY ANY CODE BENEATH THIS LINE ######
    ######################################################

    def get_turn(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns the turn of the person.
        """
        return self.turn

    def get_current_floor(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns the current_floor of the person.
        """
        return self.current_floor

    def get_target_floor(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns the target_floor of the person.
        """
        return self.target_floor

    def get_anger_level(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  Returns the anger_level of the person.
        """
        return self.anger_level

    def __str__(self) -> str:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  returns a string of the Person attributes,
                  not including the turn

        Example:  For a Person with:
                  current_floor of 4
                  target_floor of 8
                  anger_level 3

                  This will return 'f4t8a3'
        """
        return (f"f{self.current_floor}t{self.target_floor}"
                f"a{self.anger_level}")
