"""Module that contains the functions used to set up the components of the game
for all versions of it, command-line and web-based."""
import random
import json
import re
import logging
logging.basicConfig(filename = 'battleships.log', encoding='utf-8',
                    level=logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s'
                    ,datefmt='%Y-%m-%d %H:%M:%S')

def initialise_board(size: int = 10) -> list[list]:
    """Function used to initialise the board
    
    :param size: an integer value representing the size of the board
    """
    board = []
    # The loop will continue generating the board until it reaches the value of size
    for _ in range(size):
        board += [[None] * size]
    return board

def create_battleships(filename: str = "battleships.txt")-> dict[str, int]:
    """Function used to retrieve each battle ship and their size
    
    :param filename: a string value containing the name of the txt file 
    containing the name of the ships with their respective size
    """
    battleships = {}
    # Opens the battleships.txt file and returns the name of the ship and the size
    # and is seperated by the ',' delimeter
    with open(filename, "r", encoding = "utf-8") as my_file:
        content = my_file.readlines()
        for line in content:
            pattern = r'^\w+,\d+$'
            if not re.match(pattern, line):
                print("Invalid battleships.txt configuration. Please enter"
                      " the ships in the format: ship_name,length_of_ship")
                logging.error("The ships were not processed as it was not in the correct format.")
                raise ValueError("Invalid battleships.txt configuration."
                      "\nThe ships must be in the format: ship_name,length_of_ship"
                      "\nThe length of the ship represents an integer value.")
            line = line.replace("\n", "")
            battleship, length = line.strip().split(',')
            battleships[battleship] = int(length)
    if not battleships:
        logging.error("The battleship.txt file is empty")
        raise ValueError("The battleships.txt file is empty")
    return battleships

def check_ways_to_place(length: str, board: list[list]) -> [str, str, str]:
    """Function used check which orientation is possible for each ship to be placed on the board.
    
    :param length: a string value containing the length of each ship from the battleships.txt file
    :param board: a nested list of length (default 10 but it depends of 
    size parameter in initialise_board function) representing the layout of a board
    """
    ways_to_place = []
    #Starting position for generation
    row_index = random.randint(0,len(board) - 1)
    column_index = random.randint(0,len(board) - 1)
    testing_row = row_index
    testing_column = column_index
    #Right Check
    if column_index + int(length) <= len(board) - 1:
        for _ in range(int(length)):
            if board[testing_row][testing_column] is None:
                testing_column += 1
                valid = True
            else:
                valid = False
                break
        #If the ship can be generated from the left to the right, then it is added to the list
        if valid is True:
            ways_to_place.append("right_check")
    #Left Check
    testing_row = row_index
    testing_column = column_index
    if column_index - int(length) >= 0:
        for _ in range(int(length)):
            if board[testing_row][testing_column] is None:
                testing_column -= 1
                valid = True
            else:
                valid = False
                break
        #If the ship can be generated from the right to the left, then it is added to the list
        if valid is True:
            ways_to_place.append("left_check")
    #Down Check
    testing_row = row_index
    testing_column = column_index
    if row_index + int(length) <= len(board) - 1:
        for _ in range(int(length)):
            if board[testing_row][testing_column] is None:
                testing_row += 1
                valid = True
            else:
                valid = False
                break
        #If the ship can be generated from the up to down, then it is added to the list
        if valid is True:
            ways_to_place.append("down_check")
    #Up Check
    testing_row = row_index
    testing_column = column_index
    if row_index - int(length) >= 0:
        for _ in range(int(length)):
            if board[testing_row][testing_column] is None:
                testing_row -= 1
                valid = True
            else:
                valid = False
                break
        #If the ship can be generated from the down to up, then it is added to the list
        if valid is True:
            ways_to_place.append("up_check")
    #If there are no ways to place the ship, it will return an empty string
    if not ways_to_place:
        logging.info("No arrangements were found for the ships on this iteration")
        return []
    else:
        #Returns which ways are possible, the starting row index and the starting column index
        logging.info("Arragements were found for the ships on this iteration")
        return [ways_to_place, row_index, column_index]

def place_battleships(board: list[list], ships: dict, algorithm = 'simple')-> list[list]:
    """Function used to update the board data structure to position the ships 
    on the board
    
     :param board: a nested list of length (default 10 but it depends of size 
     parameter in initialise_board function) representing the layout of a board
     :param ships: a dictionary value containing the name of each ship as the key 
     and the size of the ship as the respective values
     :param algorithm: a string value with default value of 'simple' that 
     can be extended to include more sophisticated algorithms for placing ships 
    """
    if algorithm.lower() == 'simple':
        row_index = 0
        for battleship, length in ships.items():
            for column_index in range(int(length)):
                board[row_index][column_index] = battleship
            row_index += 1
    elif algorithm.lower() == "random":
        for battleship, length in ships.items():
            # orientation will contain the ways in which the ship can be placed
            orientation = check_ways_to_place(length, board)
            #While the return value of orientation is an empty
            #string, it will keep on trying random positions until finding a correct orientation
            while not orientation:
                orientation = check_ways_to_place(length, board)
            choice = random.choice(orientation[0])
            row_index = int(orientation[1])
            column_index = int(orientation[2])
            # Once the orientation is found, it will place the ship
            # (starting from the column and row index), and stop once
            # the length of the ship has been placed
            for _ in range(int(length)):
                if choice == "right_check":
                    board[row_index][column_index] = battleship
                    column_index += 1
                elif choice == "left_check":
                    board[row_index][column_index] = battleship
                    column_index -= 1
                elif choice == "down_check":
                    board[row_index][column_index] = battleship
                    row_index += 1
                elif choice == "up_check":
                    board[row_index][column_index] = battleship
                    row_index -= 1
    elif algorithm.lower() == 'custom':
        try:
            with open('placement.json', 'r', encoding = "UTF-8") as file:
                placement_data = json.load(file)
            for battleship, data_about_ships in placement_data.items():
                start_of_column, start_of_row, orientation = data_about_ships
                row_index = int(start_of_row)
                column_index = int(start_of_column)
                # Data validation, if the data is valid then the
                # valid_data variable will be assigned true
                valid_data = False
                if valid_data is False:
                    if not isinstance(start_of_row, str) or not isinstance(start_of_column, str):
                        logging.error("TypeError - Input co-ordinates must be "
                                      "numbers in string format")
                        raise TypeError("Input co-ordinates must be numbers in string format")
                    elif (not isinstance(int(start_of_row), int)
                    or not isinstance(int(start_of_column), int)):
                        logging.error("TypeError - Input co-ordinates must be numbers")
                        raise TypeError("Input co-ordinates must be numbers")
                    elif int(start_of_row) < 0 or int(start_of_column) < 0:
                        logging.error("ValueError - Input co-ordinates must be positive numbers")
                        raise ValueError("Input co-ordinates must be positive")
                    elif int(start_of_row) >= len(board) or int(start_of_column) >= len(board):
                        logging.error("IndexError - Input co-ordinates will generate outside of the"
                                      "boards' bounds")
                        raise IndexError("Input co-ordinates are too large for the board size")
                    else:
                        valid_data = True
                if valid_data is True:
                    #Changing to integer value so the list can be iterated through
                    row_index = int(start_of_row)
                    column_index = int(start_of_column)
                    for dictionary_ship, length in ships.items():
                        #Validation to ensure the names in battleships.txt are in the dictionary
                        if battleship in ships.keys():
                            if dictionary_ship == battleship:
                                if orientation == "h":
                                    #Data Validation if the user's placement is wrong
                                    if (column_index + length - 1) >= len(board):
                                        logging.error("IndexError - Change the arrangement"
                                                    " of the ships")
                                        raise IndexError("Please change the arrangement of your"
                                                         " ships,they are generating out of "
                                                            "the boards' bounds.")
                                    for _ in range(int(length)):
                                        if (board[row_index][column_index] is not None
                                            and board[row_index][column_index] != battleship):
                                            logging.error("ValueError - Change the"
                                                          " ship arrangements")
                                            raise ValueError("Change your ship arrangements "
                                                            "as differing ships "
                                                            "overlap each other.")
                                        else:
                                            board[row_index][column_index] = battleship
                                            column_index += 1
                                elif orientation == "v":
                                    if (row_index + length - 1) >= len(board):
                                        logging.error("IndexError - Change the arrangement"
                                                    " of the ships")
                                        raise IndexError("Please change the arrangement of your "
                                                         "ships,they are generating out of "
                                                            "the boards' bounds.")
                                    elif (column_index) >= len(board):
                                        logging.error("IndexError - Change the arrangement"
                                                    " of the ships")
                                        raise IndexError("Please change the arrangement of your "
                                                         "ships,they are generating out of "
                                                            "the boards' bounds.")
                                    for _ in range(int(length)):
                                        if (board[row_index][column_index] is not None
                                            and board[row_index][column_index] != battleship):
                                            logging.error("ValueError - Change the "
                                                          "ship arrangements")
                                            raise ValueError("Change your ship arrangements as "
                                                            "differing ships overlap each other.")
                                        else:
                                            board[row_index][column_index] = battleship
                                            row_index += 1
                        else:
                            logging.error("ValueError - The name of the battleship in"
                                          " the battleships.txt file\n does not match the" 
                                          " name of the ship in the placement.json file.")
                            raise ValueError("ValueError - The name of the battleship in"
                                          " the battleships.txt file\n does not match the" 
                                          " name of the ship in the placement.json file.")
        except FileNotFoundError as e:
            logging.error("Json file not found")
            raise FileNotFoundError("Json file not found") from e
    elif algorithm.lower() == "strategic":
        try:
            with open('strategic_placements.json', 'r', encoding = "UTF-8") as file:
                placement_data = json.load(file)
                placement = random.choice(placement_data)
            for battleship, data_about_ships in placement.items():
                start_of_column, start_of_row, orientation = data_about_ships
                row_index = int(start_of_row)
                column_index = int(start_of_column)
                # Data validation, if the data is valid then
                #the valid_data variable will be assigned true
                valid_data = False
                if valid_data is False:
                    if not isinstance(start_of_row, str) or not isinstance(start_of_column, str):
                        logging.error("TypeError - Input co-ordinates must"
                                      " be numbers in string format")
                        raise TypeError("Input co-ordinates must be numbers in string format")
                    elif (not isinstance(int(start_of_row), int)
                    or not isinstance(int(start_of_column), int)):
                        logging.error("TypeError - Input co-ordinates must be numbers")
                        raise TypeError("Input co-ordinates must be numbers")
                    elif int(start_of_row) < 0 or int(start_of_column) < 0:
                        logging.error("ValueError - Input co-ordinates must be positive numbers")
                        raise ValueError("Input co-ordinates must be positive")
                    elif int(start_of_row) >= len(board) or int(start_of_column) >= len(board):
                        logging.error("IndexError - Input co-ordinates will generate outside of the"
                                      "boards' bounds")
                        raise IndexError("Input co-ordinates are too large for the board size")
                    else:
                        valid_data = True
                if valid_data is True:
                    row_index = int(start_of_row)
                    column_index = int(start_of_column)
                    for dictionary_ship, length in ships.items():
                        if battleship in ships.keys():
                            if dictionary_ship == battleship:
                                if orientation == "h":
                                    #Data Validation if the user's placement is wrong
                                    if (column_index + length - 1) >= len(board):
                                        logging.error("IndexError - Change the arrangement "
                                                    "of the ships")
                                        raise IndexError("Please change the arrangement "
                                                         "of your ships"
                                                    ",they are generating out of "
                                                    "the boards' bounds.")
                                    for _ in range(int(length)):
                                        if board[row_index][column_index] is not None:
                                            logging.error("ValueError - Change the "
                                                          "ship arrangements")
                                            raise ValueError("Change your ship arrangements "
                                                            "as differing ships "
                                                            "overlap each other.")
                                        else:
                                            board[row_index][column_index] = battleship
                                            column_index += 1
                                elif orientation == "v":
                                    if (row_index + length - 1) >= len(board):
                                        logging.error("IndexError - Change the arrangement "
                                                    "of the ships")
                                        raise IndexError("Please change the arrangement "
                                                         "of your ships,they "
                                                         "are generating out of "
                                                         "the boards' bounds.")
                                    elif (column_index) >= len(board):
                                        logging.error("IndexError - Change the arrangement"
                                                    " of the ships")
                                        raise IndexError("Please change the arrangement "
                                                         "of your ships,"
                                                            " they are generating out of "
                                                            "the boards' bounds.")
                                    for _ in range(int(length)):
                                        if board[row_index][column_index] is not None:
                                            logging.error("ValueError - Change the "
                                                          "ship arrangements")
                                            raise ValueError("Change your ship arrangements"
                                                        " as differing ships overlap each other.")
                                        else:
                                            board[row_index][column_index] = battleship
                                            row_index += 1
                        else:
                            logging.error("ValueError - The name of the battleship in"
                                          " the battleships.txt file\n does not match the" 
                                          " name of the ship in the placement.json file.")
                            raise ValueError("ValueError - The name of the battleship in"
                                          " the battleships.txt file\n does not match the" 
                                          " name of the ship in the placement.json file.")
        except FileNotFoundError as e:
            logging.error("Json file not found")
            raise FileNotFoundError("Json file not found") from e
    return board
