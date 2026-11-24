"""
Game.py

Copyright 2026 University of Michigan EECS183

Evan Roetman
evancr

Priyom Chowdhury
priyomc

Logan Santana
santalog

Abid Chowdhury
abidchow

EECS 183 (Python): Final Project - Elevators
"""

from copy import deepcopy
from typing import TextIO
from Move import Move
from Person import Person
from Building import Building
from SatisfactionIndex import SatisfactionIndex
from AI import get_ai_move_string, get_ai_pickup_list
from Utility import (
    NUM_ELEVATORS,
    NUM_FLOORS,
    LOAD_FILENAME,
    GAME_INPUT_FILENAME,
    MAX_TURNS,
    ELEVATOR_CAPACITY,
    IS_AI_OVERRIDE,
)

import sys
import random
from enum import Enum

from pathlib import Path
BASE_DIR = Path(__file__).parent


class IntroChoice(int, Enum):
    Run_Tests = 0
    Load = 1
    New = 2


class AIChoice(int, Enum):
    Human = 1
    AI = 2


class GameChoice(str, Enum):
    Quit = "Q"
    Save = "S"
    Move = "e"
    # Cannot use "Pass" as it's a Python keyword
    Pass_ = ""


class QuitChoice(int, Enum):
    Quit = 1
    Stay = 2


class Game:
    def __init__(self) -> None:
        # Do not modify this method
        self.building = Building()
        self.satisfaction_index = SatisfactionIndex()
        self.is_ai_mode: bool = False

    def play_game(self, is_ai_mode_in: bool, game_file: TextIO) -> None:
        """
        Requires: Nothing
        Modifies: is_ai_mode, building, satisfaction_index
        Effects:  sets is_ai_mode
                  prints game start prompt
                  initializes the game with the game_file
                  reads events from game input file
                  if event is happening on current turn, updates building
                  with event else prints building and checks if game has
                  ended, if it hasn't yet, gets user (player or AI) move,
                  and updates building with move.

        Note: all of the event strings may have been read from the file
              before check_for_game_end ends the game
        """
        
        self.is_ai_mode = is_ai_mode_in
        self.print_game_start_prompt()
        self.init_game(game_file)

        for line in game_file:
            line = line.strip()

            if line == "":
                continue

            person = Person(line)
            spawn_time = person.get_turn()

            while self.building.get_time() < spawn_time:
                self.building.pretty_print_building()
                self.satisfaction_index.print_satisfaction()
                self.check_for_game_end()

                next_move = self.get_move()
                self.update(next_move)

            self.building.spawn_person(person)

        while True:
            self.building.pretty_print_building()
            self.satisfaction_index.print_satisfaction()
            self.check_for_game_end()

            next_move = self.get_move()
            self.update(next_move)

    def is_valid_pickup_list(
            self, pickup_list: str, pickup_floor_num: int
        ) -> bool:
            """
            Requires: pickup_floor_num is the floor the pickup move was called on
            Modifies: Nothing
            Effects:  determines if pickup_list is a valid
                    list of people to pick up
            """
        
            pickup_floor = self.building.get_floor_by_floor_num(pickup_floor_num)

            def no_duplicates(str: str) -> bool:
                '''
                Requires: Nothing
                Modifies: Nothing
                Effects:  Returns True if there are no duplicates in str, otherwise
                        returns False
                '''
                for reference_char in str:
                    count = 0
                    for checked_char in str:
                        if checked_char == reference_char:
                            count += 1
                    if count > 1:
                        return False
                return True

            def is_strict_digits(str: str) -> bool:
                '''
                Requires: Nothing
                Modifies: Nothing
                Effects:  Returns True if all characters in str are digits 0-9,
                        otherwise returns False
                '''
                for char in str:
                    if char not in list('0123456789'):
                        return False
                return True

            def max_less_than_num_people_floor(
                digits: str,
                num_people: int
            ) -> bool:
                '''
                Requires: All characters in digits are convertible to int
                Modifies: Nothing
                Effects:  Returns True if the maximum digit in digits is less than
                        num_people, otherwise returns False
                '''
                ints = [int(char) for char in digits]
                return max(ints) < num_people

            def all_same_direction(pickup_list) -> bool:
                '''
                Requires: No person is traveling to their own floor
                Modifies: Nothing
                Effects:  Checks whether each person referenced by pickup_list is
                        going up or down; returns True if they are all the same,
                        otherwise returns False.
                '''
                overall_direction = None
                person_direction = ''
                for p_idx in [int(char) for char in pickup_list]:
                    person = pickup_floor.get_person_by_index(p_idx)
                    if (person.get_target_floor() - pickup_floor_num) > 0:
                        person_direction = 'up'
                    elif (person.get_target_floor() - pickup_floor_num) < 0:
                        person_direction = 'down'
                    else:
                        raise Exception('Person traveling to their own floor.')
                    if (
                        overall_direction != person_direction
                        and overall_direction is not None
                    ):
                        return False
                    overall_direction = person_direction
                return True
           
            return (
                no_duplicates(pickup_list)
                and is_strict_digits(pickup_list)
                and len(pickup_list) <= ELEVATOR_CAPACITY
                and max_less_than_num_people_floor(
                    pickup_list,
                    pickup_floor.get_num_people()
                )
                and all_same_direction(pickup_list)
            )

    ######################################################
    ###### DO NOT MODIFY ANY CODE BENEATH THIS LINE ######
    ######################################################

    def perform_move(self, move: Move) -> bool:
        """
        Requires: move has been given a user inputted move
        Modifies: move
        Effects:  if move is not valid, returns false
                  if move is a pickup move and a pickup can be performed
                      gets people to be picked up
                      otherwise returns false
                  otherwise returns true
        """
        # create list of elevator objects
        elevators = [
            self.building.get_elevator_by_id(i)
            for i in range(NUM_ELEVATORS)
        ]

        if move.is_valid_move(elevators) and move.is_pickup_move():
            elev_id = move.get_elevator_id()
            tagged_elevator = self.building.get_elevator_by_id(
                elev_id
            )
            tagged_floor = self.building.get_floor_by_floor_num(
                tagged_elevator.get_current_floor()
            )

            if tagged_floor.get_num_people() > 0:
                # this will interactively ask for pickup
                # choices (or AI override)
                self.get_people_to_pickup(move)
                return True

            return False
        elif move.is_save_move():
            self.perform_save()
        elif move.is_quit_move():
            self.perform_quit()
        elif not move.is_valid_move(elevators):
            return False

        return True

    def print_welcome_menu(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints welcome banner
        """
        print('########################################')
        print('# Welcome to EECS 183 Elevator Escape! #')
        print('########################################')
        print()

    def print_intro_menu(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints intro choice menu
        """
        print('[0] Run Tests')
        print('[1] Load saved game')
        print('[2] Start new game')
        print('Choice: ', end='')

    def print_ai_menu(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints ai choice menu
        """
        print('[1] Play as human')
        print('[2] Watch AI play')
        print('Choice: ', end='')

    def print_options(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints the user options
        """
        print('########################################')
        print('#         Enter service move:          #')
        print("#     'e' elevator_id 'f' floor_num      #")
        print('#            Or pickup move:           #')
        print("#          'e' elevator_id 'p'          #")
        print('########################################')

    def print_game_start_prompt(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints game start prompt
                 pauses until further input received
        """
        print()
        print('########################################')
        print('#                 Enter:               #')
        print('#               Q to Quit              #')
        print('#               S to Save              #')
        print('#      At any time after this prompt   #')
        print('########################################')
        print()
        print('Press enter to continue....', end='')
        try:
            input()
        except EOFError:
            # if input isn't available, continue
            pass
        print()

    def print_satisfaction_index(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints satisfaction_index
        """
        print()
        print()
        print('Your hotel\'s current satisfaction index is: ', end='')
        # satisfaction_index defines __str__ or has print_satisfaction
        self.satisfaction_index.print_satisfaction()
        print()
        print()

    def get_intro_choice(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints the intro menu
                 reads the input from the user
                 checks to make sure the input is within range for the menu
                 if not, prints "Invalid menu choice!"
                 continues to print the menu and read an input until
                 a valid one is entered
                 returns the users choice of menu options
        """
        if IS_AI_OVERRIDE:
            # IntroChoice::New == 2
            return 2

        choice = -1
        while choice < 0 or choice > 2:
            self.print_intro_menu()
            s_choice = input()
            try:
                choice = int(s_choice)
            except ValueError:
                choice = -1

            if choice < 0 or choice > 2:
                print()
                print('Invalid menu choice!')
                print()

        print()
        return choice  # caller can map 0/1/2 to enum if desired

    def get_ai_choice(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints the ai menu
                 reads the input from the user
                 checks to make sure the input is within range for the menu
                 if not, prints "Invalid menu choice!"
                 continues to print the menu and read an input until
                 a valid one is entered
                 returns the users choice of menu options

        Prompts: "Invalid menu choice!"
        """
        if IS_AI_OVERRIDE:
            # AIChoice::AI == 2
            return 2

        self.print_ai_menu()
        s_choice = input()
        try:
            choice = int(s_choice)
        except ValueError:
            choice = 0

        while choice != 1 and choice != 2:
            print()
            print('Invalid menu choice!')
            print()
            s_choice = input()
            try:
                choice = int(s_choice)
            except ValueError:
                choice = 0

        print()
        return choice  # 1 -> Human, 2 -> AI

    def get_move(self) -> Move:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  if ai is playing
                      gets building state and gives to ai
                      if ai requests pickup move, builds list of people
                      on requested floor and gives list back to ai
                      returns ai move
                  else gets user move and returns it

        Note: This function has been implemented for you
        """
        move_obj = Move()
        move_string = ''
        is_valid = False

        # sentinel for invalid char; mimic GameChoice::Invalid
        while not is_valid:
            print('Enter move: ', end='')
            move_string = input()
            print()

            if self.is_ai_mode:
                move_string = get_ai_move_string(
                    self.building.get_building_state()
                )
                print(f'AI OVERRIDE: {move_string}')

            move_obj = Move(move_string)

            # if empty string, pass move
            if move_string == '':
                return move_obj
            else:
                choice_capture = move_string[0]

            if choice_capture in ('Q', 'q'):
                self.perform_quit()
            elif choice_capture in ('S', 's'):
                is_valid = self.perform_save()
            elif choice_capture == 'e':
                is_valid = self.perform_move(move_obj)
            else:
                is_valid = False

            if not is_valid:
                print()
                print('Invalid move!')
                print()
                self.check_for_game_end()

        return move_obj

    def perform_quit(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  asks the user if they want to quit the game
                  if yes, ends the game immediately
                  otherwise returns
        """
        quit_choice = self.get_exit_choice()
        if quit_choice == 1:
            # QuitChoice::Quit
            self.end_game()
        elif quit_choice == 2:
            # Stay -> return to caller
            return

    def perform_save(self) -> bool:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  attempts to save the game
                  if save file could not be opened,
                      prompts 'Could not open <filename>' and returns false

                  returns true on success, false otherwise

        Prompts: 'Could not open <filename>'
        """
        try:
            save_file = open(BASE_DIR / LOAD_FILENAME, 'w')
        except OSError:
            print(f'Could not open {LOAD_FILENAME}')
            return False

        try:
            result = self.save_game(save_file)
        finally:
            save_file.close()
        return result

    def get_people_to_pickup(self, move: Move) -> None:
        """
        Requires: move is a pickup move
        Modifies: move
        Effects:  prints floor pickup menu of floor move is taken from
                  reads the input from the user
                  checks to make sure pickup choices are valid
                  if not prints "Invalid list of people chosen!"
                  continues to print menu and read an input until
                  valid one is entered
                  updates move to contain correct list of people to pick up
                  updates move to contain the new target floor from
                  the people picked up

        Prompts: "Invalid list of people chosen!"
        """
        elev_id = move.get_elevator_id()
        current_floor_num = (
            self.building.get_elevator_by_id(
                elev_id
            ).get_current_floor()
        )
        current_floor = self.building.get_floor_by_floor_num(current_floor_num)

        if current_floor.get_num_people() == 1:
            move.set_people_to_pickup('0', current_floor_num, current_floor)
            return

        people_indices = ''
        is_valid_pickup = False

        while not is_valid_pickup:
            # prints floor pickup menu to stdout
            current_floor.print_floor_pickup_menu()
            print()
            print('Choices: ', end='')
            people_indices = input()
            print('\n')

            if self.is_ai_mode:
                e = self.building.get_elevator_by_id(
                    move.get_elevator_id()
                )
                f_live = self.building.get_floor_by_floor_num(
                    e.get_current_floor()
                )
                people_indices = get_ai_pickup_list(
                    deepcopy(move),
                    self.building.get_building_state(),
                    deepcopy(f_live)
                )
                print(f'AI OVERRIDE: {people_indices}')

            is_valid_pickup = self.is_valid_pickup_list(
                people_indices, current_floor_num
            )

            if not is_valid_pickup:
                print('Invalid list of people chosen!')
                self.check_for_game_end()

        move.set_people_to_pickup(
            people_indices, current_floor_num, current_floor
        )

    def init_game(self, load_file: TextIO) -> None:
        """
        Requires: load_file is in good state
        Modifies: satisfaction_index, building
        Effects:  prints "Loading game..."
                  reads from load_file the state of the game
                  updates current game to be the new state
                  prints "Loaded!" when finished

        Prompts: "Loading game..."
                 "Loaded!"
        """
        print()
        print('Loading game...')
        print()

        # Read raw satisfaction
        # Expect 5 lines (one per raw satisfaction value)
        try:
            vals = []
            for _ in range(5):
                line = load_file.readline()
                if line == '':
                    raise EOFError
                vals.append(int(line.strip()))
            # assign to satisfaction_index fields (assumes method exists)
            self.satisfaction_index.read_raw_satisfaction(vals)

            # read time
            temp_time_line = load_file.readline()
            if temp_time_line == '':
                raise EOFError
            temp_time = int(temp_time_line.strip())
            self.building.set_time(temp_time)

            # read elevator states: up to NUM_ELEVATORS tokens/lines
            i = 0
            while i < NUM_ELEVATORS:
                elev_state = load_file.readline()
                if elev_state == '':
                    break
                elev_state = elev_state.strip()
                if elev_state == '':
                    # skip blank lines
                    continue
                self.building.set_elevator(elev_state, i)
                i += 1

            # check for failure
            # We treat a short read as failure
            if load_file is not None:
                print('Loaded!')
                print()
            else:
                # unreachable, kept to match the original control flow
                print()
                print('Error when loading the file! Verify that '
                      'you have correctly created your project.')
                print()
                print('You will need to fix this before'
                      ' implementing Game::play_game or the '
                      'Reach AI.')
                print()
                print('Press enter to continue....', end='')
                try:
                    input()
                except EOFError:
                    pass
                print()
        except Exception:
            # any parsing/IO error -> show error
            print()
            print('Error when loading the file! Verify that '
                  'you have correctly created your project.')
            print()
            print('You will need to fix this before implementing '
                  'Game::play_game or the Reach AI.')
            print()
            print('Press enter to continue....', end='')
            try:
                input()
            except EOFError:
                pass
            print()

        return

    def print_exit_menu(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  prints the exit menu
        """
        print()
        print('Are you sure you want to quit?')
        print('[1] Yes, I\'m sure!')
        print('[2] No, keep playing!')
        print('Choice: ', end='')

    def get_exit_choice(self) -> int:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  prints the exit menu
                  reads the input from the user
                  checks to make sure the input is within range for the menu
                  if not, prints "Invalid menu choice!"
                  continues to print the menu and read an input until
                  a valid one is entered
                  returns the users choice of menu options

        Prompts: "Invalid menu choice!"
        """
        exit_choice = 0
        while exit_choice < 1 or exit_choice > 2:
            self.print_exit_menu()
            choice = input()
            try:
                exit_choice = int(choice)
            except ValueError:
                exit_choice = 0

            if exit_choice < 1 or exit_choice > 2:
                print()
                print('Invalid menu choice!')
                print()

        print()
        return exit_choice

    def end_game(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  prints "Goodbye!" and
                  exits program with status code 0

        Prompts: "Goodbye!"
        """
        print()
        print('Goodbye!')
        # attempt to save satisfaction index like original
        try:
            self.satisfaction_index.save()
        except Exception:
            # ignore save errors here
            # (just call and exit)
            pass
        sys.exit(0)

    def print_success_ending(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints success ending prompt
        """
        print()
        print()
        print('Time is up! Your final score is: ')
        self.satisfaction_index.print_satisfaction()

    def print_failure_ending(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects: prints failure ending prompt
        """
        print()
        print()
        print('Uh oh! Your hotel has gone out of business!')
        print('Better luck next time!')
        print()
        print('Your final achievement:')
        print()
        self.satisfaction_index.print_satisfaction()

    def check_for_game_end(self) -> None:
        """
        Requires: Nothing
        Modifies: Nothing
        Effects:  checks if the game has ended.
                  If the game has ended, calls either:

                  print_success_ending or
                  print_failure_ending

                  depending on how the game ended.
                  If the game has ended, calls end_game();
        """
        if self.building.get_time() >= MAX_TURNS:
            self.print_success_ending()
            self.end_game()
        elif self.satisfaction_index.get_satisfaction() < 0:
            self.print_failure_ending()
            self.end_game()

    def update(self, m: Move) -> None:
        """
        Requires: move is a valid move
        Modifies: building, satisfaction_index
        Effects:  If move is a pickup move
                      increases satisfaction index
                      according to the people picked up
                  calls building.tick on move
                  reduces satisfaction index
                  by factor of those exploded this turn (returned by tick)
                  finally, on every other tick (when the new building time
                  is odd), updates idle benchmark according to idle
                  elevators
        """
        # Save/quit are control actions and should not advance simulation.
        if m.is_save_move() or m.is_quit_move():
            return

        if m.is_pickup_move():
            self.satisfaction_index.update_sum_direction_request(
                m, self.building
            )
        self.satisfaction_index.update_sum_exploded(self.building.tick(m))
        self.satisfaction_index.update_time_reached(self.building)
        if self.building.get_time() % 2:
            self.satisfaction_index.update_sum_idle(self.building)

    def save_game(self, save_file: TextIO) -> bool:
        """
        You will *not* implement this function for the project

        Requires: save_file is in good state
        Modifies: save_file
        Effects:  prints 'Saving game...'
                  adds current state of game to save_file
                  reads remaining moves from game input file
                  if game input file cannot be opened
                      prints 'Game input file could not be opened!'
                      and returns false
                  else
                      adds remaining move to save_file
                      flushes save_file buffer
                      prints 'Saved!' when finished and returns true

        Prompts: 'Saving game...'
                 'Saved!'
                 'Game input file could not be opened!'
        """
        print('Saving game...', end='')

        try:
            save_file.write(f'{self.satisfaction_index.sum_index}\n')
            save_file.write(f'{self.satisfaction_index.sum_up_request}\n')
            save_file.write(f'{self.satisfaction_index.sum_down_request}\n')
            save_file.write(f'{self.satisfaction_index.sum_exploded}\n')
            save_file.write(f'{self.satisfaction_index.sum_idle}\n')
        except Exception:
            # ignore and continue
            pass

        time = self.building.get_time()
        save_file.write(f'{time}\n')

        for i in range(NUM_ELEVATORS):
            e = self.building.get_elevator_by_id(i)
            save_file.write(str(e) + '\n')

        for floor_i in range(NUM_FLOORS):
            f = self.building.get_floor_by_floor_num(floor_i)
            num_peeps = f.get_num_people()
            for p_idx in range(num_peeps):
                save_file.write('0')
                person = f.get_person_by_index(p_idx)
                save_file.write(str(person) + '\n')

        # Append remaining events from GAME_INPUT_FILENAME
        try:
            with open(BASE_DIR / GAME_INPUT_FILENAME, 'r') as in_file:
                # skip first 6 + NUM_ELEVATORS lines
                skip_lines = 6 + NUM_ELEVATORS
                for _ in range(skip_lines):
                    _ = in_file.readline()

                # transfer remaining lines if their time > current time
                while True:
                    line = in_file.readline()
                    if line == '':
                        break
                    token = line.strip()
                    if token == '':
                        continue
                    peep = Person(token)
                    if peep.get_turn() > time:
                        save_file.write(token + '\n')
        except Exception:
            print('Game input file could not be opened!')
            return False

        save_file.flush()
        print('Saved!')
        return True
