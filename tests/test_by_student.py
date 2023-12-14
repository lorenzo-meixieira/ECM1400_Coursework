import pytest
import os
import inspect
import components
import game_engine
import mp_game_engine
import tests.test_helper_functions as thf
testReport = thf.TestReport("test_report.txt")

########################################################################################################################
# Test Components.py functions
########################################################################################################################
def test_initialise_board_values():
    """
    Test if the initialise_board function has all None values returned when this function is run.
    """

    size = 10
    board = components.initialise_board(10)
    #Checks that every value in each row is None
    for row in range(size):
        for column in range(size):
            assert board[row][column] is None

def test_check_ways_to_place_exists():
    """
    Test if the check_ways_to_place method exists.
    """
    try:
        assert hasattr(components, 'check_ways_to_place'), "check_ways_to_place function does not exist"
    except AssertionError:
        testReport.add_message("initialise_board function does not exist in your solution.")

def is_list_of_three_strings_or_empty(obj):
    """
    Used to test if an object is a list containing either 3 strings or is an empty list
    """
    if not isinstance(obj, list):
        return False
    if len(obj) == 0:
        return True  # Empty list is allowed
    if len(obj) != 3:
        return False
    if not all(isinstance(item, str) for item in obj):
        return False
    return True

def test_create_battleships_has_all_ships_from_battleships_txt_file():
    """
    Test if the create_battleships function actually returns the expected battleships from the battleships.txt file
    """
    # Call the function that returns the actual dictionary
    actual_battleships = components.create_battleships()
    # Define the expected dictionary
    expected_battleships = {
        'Aircraft_Carrier': 5,
        'Battleship': 4,
        'Cruiser': 3,
        'Submarine': 3,
        'Destroyer': 2
    }

    # Check if the keys match
    assert set(actual_battleships.keys()) == set(expected_battleships.keys()), "Keys don't match"

    # Check if the sizes of battleships match
    for ship, size in expected_battleships.items():
        assert actual_battleships[ship] == size, f"Size of {ship} is not as expected"

    # Check the lengths of dictionaries to ensure they are the same
    assert len(actual_battleships) == len(expected_battleships), "Length of dictionaries don't match"

    #Check if the dictionary's perfectly match
    assert actual_battleships == expected_battleships

def test_placement_json_exists():
    """
    Test if the placement.json file exists.
    """
    file_path = 'placement.json'

    assert os.path.exists(file_path), f"File {file_path} does not exist"

def test_strategic_placements_json_exists():
    """
    Test if the strategic_placements.json file exists.
    """
    file_path = 'strategic_placements.json'

    assert os.path.exists(file_path), f"File {file_path} does not exist"

########################################################################################################################
# Test Game Engine.py functions
########################################################################################################################
def test_attack_identifies_actual_hits_and_misses():
    """
    Test if attack function will correctly identify a hit and a miss 
    based on the simple algororithm for a player as an easy example
    """

    ships = components.create_battleships()
    board = components.place_battleships(components.initialise_board(), ships, 'simple')
    hit = (0,0)
    miss = (9,9)


    assert game_engine.attack(hit, board, ships) is True
    assert game_engine.attack(miss, board, ships) is False

def test_attack_decrements_ship_once_hit():
    """
    Test if attack function will correctly decrement a ships length if it is hit (based on simple algorithm again)
    """
    ships = components.create_battleships()
    board = components.place_battleships(components.initialise_board(), ships, 'simple')
    hit = (0,0)
    game_engine.attack(hit, board, ships)

    assert ships["Aircraft_Carrier"] == 4

########################################################################################################################
# Test mp_game_engine.py functions
########################################################################################################################
    
def test_generate_attack_is_within_the_boards_bounds():
    """
    Test if the generate attack function will generate attacks that are within the bounds of the board
    """

    board_size = len(components.initialise_board()) - 1
    x, y =  mp_game_engine.generate_attack() 
    assert x <= board_size and x >= 0
    assert y <= board_size and y >= 0

def test_print_board_exists():
    """
    Test if the print board method exists.
    """
    try:
        assert hasattr(mp_game_engine, 'print_board'), "print_board function does not exist"
    except AssertionError:
        testReport.add_message("print_board function does not exist in the solution.")

def test_print_board_arguments():
    """
    Test if the print_board function accepts a list of lists representing the users board
    """
    try:
        # Check to make sure the print_board function has a board ships and algorithm argument
        assert "users_board" in inspect.signature(mp_game_engine.print_board).parameters, ("print_board function"
                                                                                       "does not have a users_board argument")
    except AssertionError:
        testReport.add_message("print_board function is missing an argument."
                               "Check the function has a users_board argument")

def test_targeting_mode_exists():
    """
    Test if the targeting_mode method exists.
    """
    try:
        assert hasattr(mp_game_engine, 'targeting_mode'), "targeting_mode function does not exist"
    except AssertionError:
        testReport.add_message("targeting_mode function does not exist in the solution.")

def test_targeting_mode_arguments():
    """
    Test if the targeting_mode function accepts a tuple with an ai_hit, a list of lists representing the users board
    and a string with the type of ship that was hit by the ai_hit
    """
    try:
        # Check to make sure the targeting_mode function has a board ships and algorithm argument
        assert "ai_hit" in inspect.signature(mp_game_engine.targeting_mode).parameters, ("targeting_mode function"
                                                                                       "does not have a ai_hit argument")
        assert "users_board" in inspect.signature(mp_game_engine.targeting_mode).parameters, ("targeting_mode function"
                                                                                       "does not have a users_board argument")
        assert "type_of_ship_hit" in inspect.signature(mp_game_engine.targeting_mode).parameters, ("targeting_mode function"
                                                                                       "does not have a type_of_ship_hit argument")
    except AssertionError:
        testReport.add_message("targeting_mode function is missing one/more arguments."
                               "Check the function has a all arguments")
