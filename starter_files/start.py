"""
start.py

SatisfactionIndex.py

EECS 183 (Python): Final Project - Elevators
"""

from pathlib import Path

from Game import Game, IntroChoice, AIChoice
from Utility import LOAD_FILENAME, NEW_FILENAME, GAME_INPUT_FILENAME
import tests

BASE_DIR = Path(__file__).parent

########################################################
######### DO NOT MODIFY ANY CODE IN THIS FILE ##########
########################################################

def main() -> int:
    game = Game()
    game.print_welcome_menu()
    intro_choice = game.get_intro_choice()

    event_source_filename = ""

    if intro_choice == IntroChoice.Run_Tests:
        tests.start_tests()
        return 0
    elif intro_choice == IntroChoice.Load:
        event_source_filename = LOAD_FILENAME
    elif intro_choice == IntroChoice.New:
        event_source_filename = NEW_FILENAME
    else:
        raise RuntimeError("ERROR: Invalid menu choice detected")

    # Copy the event file to the game input file
    with open(BASE_DIR / event_source_filename, "r") as input_file:
        lines = input_file.readlines()

    with open(BASE_DIR / GAME_INPUT_FILENAME, "w") as game_output:
        for i, line in enumerate(lines):
            game_output.write(line.rstrip("\n"))
            if i < len(lines) - 1:
                game_output.write("\n")

    # Open the game input file for reading
    with open(BASE_DIR / GAME_INPUT_FILENAME, "r") as input_file:
        ai_mode = game.get_ai_choice() == AIChoice.AI
        game.play_game(ai_mode, input_file)

    return 0


if __name__ == "__main__":
    main()
