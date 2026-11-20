"""
SatisfactionIndex.py

Copyright 2026 University of Michigan EECS183

EECS 183 (Python): Final Project - Elevators
"""

from Building import Building
from Move import Move
from Utility import POINTS_LOST_PER_EXPLOSION, RESULT_FILENAME, NUM_ELEVATORS

from pathlib import Path
BASE_DIR = Path(__file__).parent

########################################################
######### DO NOT MODIFY ANY CODE IN THIS FILE ##########
########################################################

class SatisfactionIndex:

    def __init__(self):
        """
        Requires: Nothing
        Modifies: self
        Effects:  sets all modified attributes to 0
        """
        self.sum_index = 0
        self.sum_up_request = 0
        self.sum_down_request = 0
        self.sum_exploded = 0
        self.sum_idle = 0
        self.time_reached = 0

    def get_satisfaction(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  returns sum_index
        """
        return self.sum_index

    def update_sum_direction_request(
        self, move: Move, building: Building
    ) -> None:
        """
        Requires: move and building are valid
        Modifies: sum_up_request, sum_down_request, sum_index
        Effects:  if move causes elevator to go down,
                      increments sum_down_request
                  if move causes elevator to go up,
                      increments sum_up_request
                  increments sum_index based on move satisfaction
        """
        self.sum_index += move.get_total_satisfaction()

        elev_id = move.get_elevator_id()
        elev = building.get_elevator_by_id(elev_id)
        current_elevator_floor = elev.get_current_floor()
        target_floor = move.get_target_floor()

        # Track direction requests
        if current_elevator_floor < target_floor:
            self.sum_up_request += 1
        else:
            self.sum_down_request += 1

    def update_sum_exploded(self, num: int) -> None:
        """
        Requires: Nothing
        Modifies: sum_index, sum_exploded
        Effects:  increments sum_exploded by num
                  increments sum_index by num * POINTS_LOST_PER_EXPLOSION
        """
        self.sum_exploded += num
        self.sum_index += num * POINTS_LOST_PER_EXPLOSION

    def update_sum_idle(self, building: Building) -> None:
        """
        Requires: building is valid
        Modifies: sum_idle
        Effects:  increments sum_idle by 1 for each idle elevator in building
        """
        for i in range(NUM_ELEVATORS):
            if not building.get_elevator_by_id(i).is_servicing():
                self.sum_idle += 1

    def update_time_reached(self, building: Building) -> None:
        """
        Requires: building is valid
        Modifies: time_reached
        Effects:  sets time_reached to current time of building
        """
        self.time_reached = building.get_time()

    def read_raw_satisfaction(self, values: list[int]) -> None:
        """
        Requires: Nothing
        Modifies: self (all attributes)
        Effects:  reads modified attributes in order from values list
        """
        if len(values) != 5:
            raise ValueError(
                'Expected 5 values for raw satisfaction'
            )
        (self.sum_index, self.sum_up_request,
         self.sum_down_request, self.sum_exploded,
         self.sum_idle) = values

    def print_raw_satisfaction(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  prints sum_index, sum_up_request,
                  sum_down_request, sum_exploded,
                  sum_idle in order, separated by newline
        """
        print(self.sum_index)
        print(self.sum_up_request)
        print(self.sum_down_request)
        print(self.sum_exploded)
        print(self.sum_idle)

    def print_satisfaction(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  prints sum_index, sum_up_request,
                  sum_down_request, sum_exploded,
                  sum_idle in order with labels
        """
        print(f'sum_index:      \t{self.sum_index}')
        print(f'sum_up_request:  \t{self.sum_up_request}')
        print(f'sum_down_request:\t{self.sum_down_request}')
        print(f'sum_exploded:   \t{self.sum_exploded}')
        print(f'sum_idle:       \t{self.sum_idle}')
        print(f'time_reached:   \t{self.time_reached}')

    def save(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing (writes to file)
        Effects:  saves sum_index, sum_up_request,
                  sum_down_request, sum_exploded,
                  sum_idle in csv format to RESULT_FILENAME
        """
        try:
            with open(BASE_DIR / RESULT_FILENAME, 'w') as f:
                header = ('test,sum_index,sum_up_request,'
                          'sum_down_request,sum_exploded,'
                          'sum_idle,time_reached\n')
                f.write(header)
                row = (f'student,{self.sum_index},'
                       f'{self.sum_up_request},'
                       f'{self.sum_down_request},'
                       f'{self.sum_exploded},'
                       f'{self.sum_idle},'
                       f'{self.time_reached}\n')
                f.write(row)
        except OSError:
            print(f'Error writing to {RESULT_FILENAME}')
