"""
Building.py

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

from Elevator import Elevator
from Floor import Floor
from Person import Person
from Move import Move
from BuildingState import BuildingState
from Utility import (
    NUM_ELEVATORS,
    NUM_FLOORS
)


class Building:
    def __init__(self):
        """
        Requires: Nothing
        Modifies: self
        Effects: Default initializer. Sets time to 0

        Do not modify this method
        """
        self.elevators = [Elevator() for _ in range(NUM_ELEVATORS)]
        self.floors = [Floor() for _ in range(NUM_FLOORS)]
        self.time = 0

    def spawn_person(self, new_person: Person) -> None:
        """
        Requires: new_person is a valid Person object
        Modifies: the appropriate floor in floors
        Effects:  Adds a person to the floor corresponding to the person's
                  current_floor
        """
        current_floor = new_person.get_current_floor()
        target_floor = new_person.get_target_floor()

        request = target_floor - current_floor

        self.floors[current_floor].add_person(new_person, request)

    def update(self, move: Move) -> None:
        """Update building based on move.

        Requires: move is a valid move
        Modifies: The building attributes affected by the move
        Effects: Applies the move to the building:
                 - If the move is a Pass Move, nothing happens
                 - If the move is a Pickup Move, gets the list of
                   people to pickup and calls remove_people() on
                   the appropriate floor
                 - For both Pickup Moves and Service Moves, the
                   appropriate elevator should be sent to service the
                   target_floor of the move
        """
        if move.is_pass_move():
            return

        elevator_id = move.get_elevator_id()
        elevator = self.elevators[elevator_id]

        if move.is_pickup_move():
            current_floor = elevator.get_current_floor()
            people_to_pickup = move.copy_list_of_people_to_pickup()

            self.floors[current_floor].remove_people(people_to_pickup)

        elevator.service_request(move.get_target_floor())

    def tick(self, move: Move) -> int:
        """Process one game tick.

        Requires: move is a valid move
        Modifies: The attributes of building
        Effects: Increments time and calls update() on the input move.
                 Then, ticks all of the elevators with the new time.
                 Next, ticks all of the building floors, keeping track
                 of new exploded people. Returns the total number of
                 people that exploded in this tick.
        """
        self.time += 1

        self.update(move)

        for elevator in self.elevators:
            elevator.tick(self.time)

        total_exploded = 0

        for floor in self.floors:
            total_exploded += floor.tick(self.time)

        return total_exploded

    ######################################################
    ###### DO NOT MODIFY ANY CODE BENEATH THIS LINE ######
    ######################################################

    def set_elevator(self, elevator_info: str, elevator_id: int) -> None:
        """Set elevator state from string.

        Requires: elevator_info is a well-formed info string.
                  0 <= elevator_id < NUM_ELEVATORS
        Modifies: Building's elevator at elevator_id
        Effects: Parses elevator_info and updates elevator into
                 correct state. The elevator string will come in the
                 form <num>[s<num>:w]
                 Examples: 0w, 6s8, 5w, 9s5
                 - First number: current_floor of the elevator
                 - 's': elevator is servicing, target floor is
                       number after the 's'
                 - 'w': elevator is waiting, has no target floor
                       and is ready to service requests. This is
                       used when reloading a game from a save file.
        """
        i = 0
        curr_pos_string = ""
        dest_pos_string = ""

        while elevator_info[i] not in ('s', 'w'):
            curr_pos_string += elevator_info[i]
            i += 1

        self.elevators[elevator_id] = Elevator()
        self.elevators[elevator_id].set_current_floor(int(curr_pos_string))

        if elevator_info[i] == 's':
            i += 1
            dest_pos_string = elevator_info[i:]
            self.elevators[elevator_id].service_request(int(dest_pos_string))

    def get_time(self) -> int:
        """Return current time.

        Requires: Nothing
        Modifies: Nothing
        Effects: Returns the current time for the building
        """
        return self.time

    def set_time(self, time_in: int) -> None:
        """Set current time.

        Requires: time_in >= 0
        Modifies: time
        Effects: Sets the current time for the building to time_in
        """
        self.time = time_in

    def pretty_print_building(self) -> None:
        '''
        Requires: building is in a valid state
        Modifies: print
        Effects: Prints the building state to terminal in a nice way for
                 gameplay
        '''
        for i in range(NUM_FLOORS - 1, -1, -1):
            # top border for the floor
            print('   ' + '-' * (2 * NUM_ELEVATORS + 1))

            # elevator row
            elevator_line = '   '
            for j in range(NUM_ELEVATORS):
                icon = ' '
                if (self.elevators[j].get_current_floor() == i and
                        self.elevators[j].is_servicing()):
                    icon = str(self.elevators[j].get_target_floor())
                elevator_line += '|' + icon

            elevator_line += '|'
            print(elevator_line, end='')

            # input('press enter to move from elevator_line')

            # floor line 1
            self.floors[i].pretty_print_floor_line1()
            # input('press enter to move past pretty_print_floor_line1')

            # floor number + elevator 'E' markers + any
            # left-aligned floor markers
            line = f'{i}  '
            for j in range(NUM_ELEVATORS):
                if self.elevators[j].get_current_floor() == i:
                    line += '|E'
                else:
                    line += '| '
            line += '|'
            print(line, end='')
            # input('press enter to move past this mess')

            # floor line 2
            self.floors[i].pretty_print_floor_line2()
            # input('press enter to move past pretty_print_floor_line2')

        # bottom border
        print('   ' + '-' * (2 * NUM_ELEVATORS + 1))

        # elevator indices at the bottom
        indices_line = '    ' + ' '.join(str(j) for j in range(NUM_ELEVATORS))
        print(indices_line)

    def get_elevator_by_id(self, elevator_id: int) -> Elevator:
        '''
        Requires: 0 <= elevator_id < NUM_ELEVATORS
        Modifies: Nothing
        Effects: Returns an Elevator object containing the
                 info of the elevator at index elevator_id in the building
        '''
        return self.elevators[elevator_id]

    def get_floor_by_floor_num(self, floor_num: int) -> Floor:
        '''
        Requires: 0 <= floor_num < NUM_FLOORS
        Modifies: Nothing
        Effects: Returns a Floor object containing the
                 info of the floor at index floor_num in the building
        '''
        return self.floors[floor_num]

    def get_building_state(self) -> BuildingState:
        '''
        Requires: Nothing
        Modifies: Nothing
        Effects: Returns a BuildingState object for use by AI
                 to decide its move with the same information a
                 human player would use. See BuildingState.py for more
                 info
        '''
        building_state = BuildingState()
        building_state.turn = self.time

        for i in range(NUM_FLOORS):
            floor_state = building_state.floors[i]
            floor_state.floor_num = i
            floor_state.has_down_request = (
                self.floors[i].get_has_down_request()
            )
            floor_state.has_up_request = self.floors[i].get_has_up_request()
            np_index = 0
            for j in range(self.floors[i].get_num_people()):
                p = self.floors[i].get_person_by_index(j)
                floor_state.people[np_index].anger_level = p.get_anger_level()
                np_index += 1
            floor_state.num_people = np_index

        for i in range(NUM_ELEVATORS):
            e = self.elevators[i]
            e_state = building_state.elevators[i]
            e_state.elevator_id = i
            e_state.target_floor = e.get_target_floor()
            e_state.current_floor = e.get_current_floor()
            e_state.is_servicing = e.is_servicing()

        return building_state
