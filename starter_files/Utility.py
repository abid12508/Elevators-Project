"""
Utility.py

Copyright 2026 University of Michigan EECS183

EECS 183 (Python): Final Project - Elevators
"""

######################################################################
## This file contains all of the global constants for the project.  ##
##                                                                  ##
##        DO NOT MODIFY (OR ADD) ANY CODE IN THIS FILE              ##
######################################################################

# Filenames for new game file, saved game file, and input file
NEW_FILENAME = 'new.in'
LOAD_FILENAME = 'save.in'
GAME_INPUT_FILENAME = 'game.in'
RESULT_FILENAME = 'result.csv'

# Game constants
ELEVATOR_CAPACITY = 10
NUM_FLOORS = 10
FIRST_FLOOR = 0
MAX_ANGER = 10
NUM_ELEVATORS = 3
MAX_PEOPLE_PER_FLOOR = 10
MAX_TURNS = 100

TICKS_PER_ANGER_INCREASE = 5
TICKS_PER_ELEVATOR_MOVE = 1

POINTS_LOST_PER_EXPLOSION = -10

IS_AI_OVERRIDE = False
