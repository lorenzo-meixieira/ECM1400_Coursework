"""Module that contains the functions that wil manage the 
game mechanics of the multiplayer game with an AI Opponent"""
import random
import logging
import time
import components
import game_engine
logging.basicConfig(filename = 'battleships.log', encoding='utf-8',
                    level=logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s'
                    ,datefmt='%Y-%m-%d %H:%M:%S')
players = {}


def generate_attack() -> tuple:
    """Function used for generating a tuple that will represent the attack of the AI (player 2)"""
    x_coordinate = random.randint(0,len(components.initialise_board()) - 1)
    y_coordinate = random.randint(0,len(components.initialise_board()) - 1)
    ai_attack = (x_coordinate,y_coordinate)
    return ai_attack

def targeting_mode(ai_hit: tuple, users_board: list[list], type_of_ship_hit: str) -> list[tuple]:
    """Function used for generating a list of tuples that will represent the attacks
    of the AI (player 2) to make in the next turns with advanced capabilities
    as it will find the rest of the ship
    
    :param ai_hit: a tuple containing the coordinates of a registered attack by the AI
    :param users_board: a 2D array containing the board arrangement of the player
    :param type_of_ship_hit: a string containing the name of the ship that was hit by ai_hit
    """
    attacks_with_repetition = []
    attacks_without_repetition = []
    size = len(users_board)
    #Will generate the placement of the type of shit that was hit
    for i in range(size):
        for j in range(size):
            if users_board[i][j] == type_of_ship_hit:
                ai_attack = (j, i)
                if ai_attack != ai_hit:
                    attacks_with_repetition.append(ai_attack)
    x, y = ai_hit
    x_coordinates = []
    #Extract each attacks x and y values
    for attack in attacks_with_repetition:
        x_coordinates.append(attack[0])
    #For Vertical check
    vertical_check = all(attack[0] == ai_hit[0] for attack in attacks_with_repetition)
    #If True then the ship is vertical
    if vertical_check is True:
        #It will prioritize the list by placing either side of
        # the first hit so +1 and -1 off the inital hit first and second in the list
        if y + 1 <= len(users_board) - 1:
            attacks_with_repetition.insert(0,(x, y + 1))
        if y - 1 >= 0:
            attacks_with_repetition.insert(1,(x, y - 1))
        #This will remove duplicates and after this the list will be sorted by
        #first guessing either side of the ship then the rest of the ship
        for attack in attacks_with_repetition:
            if attack not in attacks_without_repetition:
                attacks_without_repetition.append(attack)
    #If False then the ship is horizontal
    else:
        #It will prioritize the list by placing either side of
        #the first hit so +1 and -1 off the inital hit first and second in the list
        if x + 1 <= len(users_board) - 1:
            attacks_with_repetition.insert(0,(x + 1, y))
        if x - 1 >= 0:
            attacks_with_repetition.insert(1,(x - 1, y))
        #This will remove duplicates and after this the list will be sorted by
        #first guessing either side of the ship then the rest of the ship
        for attack in attacks_with_repetition:
            if attack not in attacks_without_repetition:
                attacks_without_repetition.append(attack)
    return attacks_without_repetition

def print_board(users_board: list[list]) -> str:
    """Function that will be used for generating an ascii representation of a players' board
    
    :param board: a nested list of length (default 10 but it depends of 
    size parameter in initialise_board function) representing the layout of a board
    """
    size = len(users_board)
    board = ""
    # Assigning the labels for the columns ranging from 0 to size
    board += "    " + " ".join(str(i) for i in range(size)) + "\n"

    # Assigning the top border of the board for seperation
    board += "   " + "-" * (size * 2 + 1) + "\n"

    # Assigning each row one by one
    for i in range(size):
        row = f"{i} |"
        for j in range(size):
            if users_board[i][j] is None:
                row += f" {'~'}"  # Empty ocean space where ships are not placed
            #Different symbols for each different ship
            elif users_board[i][j] == "Aircraft_Carrier":
                row += " X"
            elif users_board[i][j] == "Battleship":
                row += " O"
            elif users_board[i][j] == "Cruiser":
                row += " U"
            elif users_board[i][j] == "Submarine":
                row += " &"
            elif users_board[i][j] == "Destroyer":
                row += " #"
            else:
                row += " ?"
        # Assigning each row of the board
        board += row + " |\n"

    # Assigning the bottom border of the board for seperation
    board += "   " + "-" * (size * 2 + 1) + "\n"
    return board

def ai_opponent_game_loop() -> None:
    """Function that will be used for the game to be played through the command-line-interface"""
    print("Welcome to Battleships!")
    print("Let's get started!")
    user_board = components.initialise_board()
    ai_board = components.initialise_board()
    user_ships = components.create_battleships()
    ai_ships = components.create_battleships()
    players["Player_1"] = components.place_battleships(user_board, user_ships,"custom")
    players["AI_Player"] = components.place_battleships(ai_board, ai_ships, "random")
    user_ships_sunk = False
    ai_ships_sunk = False
    previous_ai_attacks = []
    previous_player_attacks = []
    #While the user's ships arent all sunk and the AI's ships arent all sunk
    while not user_ships_sunk or not ai_ships_sunk:
        # The user's turn
        print("It is your turn!")
        user_attack = game_engine.cli_coordinates_input()
        # User validation to check that they are not guessing the same square more than once
        while user_attack in previous_player_attacks:
            logging.warning("The user guessed the same location more than once")
            print("You have already guessed at that co-ordinate, choose another one!")
            user_attack = game_engine.cli_coordinates_input()
        previous_player_attacks.append(user_attack)
        # Process the user's attack on the AI's board
        hit_or_miss_user = game_engine.attack(user_attack, ai_board, ai_ships)
        if hit_or_miss_user:
            print("You hit the AI's ship!")
            logging.info("A ship was hit on the AI's board")
        else:
            print("You missed!")
            logging.info("No ships were hit on the AI's board")
        # Check if the AI's ships are all sunk
        ai_ships_sunk = all(value == 0 for value in ai_ships.values())
        if ai_ships_sunk:
            print("Congratulations! You sank all the AI's ships and won the game!")
            logging.info("The game has ended and the user has won in ai opponent game loop.")
            break
        # The AI opponent's turn
        print("\nAI's turn!")
        time.sleep(1)
        ai_attack = generate_attack()
        # User validation to check that the AI is not guessing the same square more than once
        while ai_attack in previous_ai_attacks:
            logging.warning("The AI guessed the same location more than once")
            ai_attack = generate_attack()
        previous_ai_attacks.append(ai_attack)
        # Process the AI's attack on the user's board
        hit_or_miss_ai = game_engine.attack(ai_attack, user_board, user_ships)
        if hit_or_miss_ai:
            print(f"AI hit your ship at {ai_attack}!")
            logging.info("A ship was hit on the user's board")
        else:
            print("AI missed!")
            logging.info("No ships were hit on the user's board")
        time.sleep(1)
        print("This is how your board looks:")
        print(print_board(user_board))
        logging.info("The board was sent to the command-line in ai opponent game loop.")
        # Check if the user's ships are all sunk
        user_ships_sunk = all(value == 0 for value in user_ships.values())
        if user_ships_sunk:
            print("AI has sunk all your ships! Game Over!")
            logging.info("The game has ended and the AI has won is ai opponent game loop.")
            break
    print("Game Over!")

if __name__ == '__main__':
    ai_opponent_game_loop()
