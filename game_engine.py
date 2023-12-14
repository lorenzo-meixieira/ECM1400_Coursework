"""Module that contains the functions that wil manage the 
game mechanics of the single player game"""
import re
import logging
import components
logging.basicConfig(filename = 'Battleships.log', encoding='utf-8',
                    level=logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s'
                    ,datefmt='%Y-%m-%d %H:%M:%S')

def attack(coordinates: tuple, board: list[list], battleships: dict) -> bool:
    """Function used to check if there is a battleship at a certain coordinate 
    on the board for the corresponding attack
    
    :param coordinates: a tuple value representing the x and y coordinate for a desired attack
    :param board: a nested list of length (default 10 but it depends of 
    size parameter in initialise_board function) representing the layout of a board
    :param battleships: a dictionary value containing the name of each ship as the key 
     and the size of the ship as the respective values
    """
    coordinate_x = int(coordinates[0])
    coordinate_y = int(coordinates[1])
    hit_or_miss = False
    # If the position of the hit contains a ship, it will decrement that ship's value by 1
    # and also replaces its position with None
    if board[coordinate_y][coordinate_x] is not None:
        type_of_ship_hit = board[coordinate_y][coordinate_x]
        battleships[type_of_ship_hit] = int(battleships[type_of_ship_hit]) - 1
        board[coordinate_y][coordinate_x] = None
        hit_or_miss = True
    else:
        hit_or_miss = False
    return hit_or_miss

def cli_coordinates_input() -> tuple:
    """Function used to retrieve where the user wants to place his attack""" 
    response = input("Enter coordinates for your attack, seperate " +
                     "each coordinate by a comma (eg 1,1)")
    #Data Validation to make sure that the user enters their guess in the correct format
    pattern = (
    f'^[0-{len(components.initialise_board()) - 1}]{{1}},'
    f'[0-{len(components.initialise_board()) - 1}]{{1}}$')
    while not re.match(pattern, response):
        print("Invalid response. Please enter your coordinate in the format x co-or, y co-or")
        logging.error("The co-ordinates were not processed as it was not in the correct format.")
        response = input("Enter coordinates for your attack, seperate each" +
    " coordinate by a comma (eg 1,1)")      
    x, y = response.split(',')
    return (int(x),int(y))

def simple_game_loop() -> None:
    """Function used for intermediate manual testing through the command-line interface"""
    print("Welcome to Battleships!")
    print("Let's get started!")
    previous_attacks = []
    ships = components.create_battleships()
    logging.info("The AI's ships for the simple game loop were created")
    board = components.place_battleships(components.initialise_board(), ships, 'simple')
    logging.info("The AI's board has been rendered in the simple game loop")
    # A check to determine if all the ships were sunk
    while all(value == 0 for value in ships.values()) is False:
        player_input = cli_coordinates_input()
        # Check to see if the attack has already been guessed
        while player_input in previous_attacks:
            logging.warning("The user guessed the same location more than once")
            print("You have already guessed at that co-ordinate, choose another one!")
            player_input = cli_coordinates_input()
        previous_attacks.append(player_input)
        if attack(player_input, board, ships) is True:
            print("Hit!")
            logging.info("A ship was hit on the AI board for this attack in simple game loop")
        else:
            print("Miss!")
            logging.info("No ship was hit the AI board for this attack in simple game loop")
    print("Game Over! All ships have been sunken")
    logging.info("The game ended in the simple game loop and the user guessed all the ships.")

if __name__ == "__main__":
    simple_game_loop()
