"""Module which is the main entry point for the project, contains functions to handle the 
webpage interfaces"""
import json
import logging
from flask import Flask, render_template, jsonify, request
import components
import game_engine
import mp_game_engine
logging.basicConfig(filename = 'battleships.log', encoding='utf-8',
                    level=logging.DEBUG, format = '%(asctime)s %(levelname)s: %(message)s'
                    ,datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
ai_board = components.initialise_board()
ai_ships = components.create_battleships()
user_board = components.initialise_board()
user_ships = components.create_battleships()
players = {}
previous_ai_attacks = []
previous_user_attacks = []

@app.route(rule = '/placement', methods = ["GET", "POST"])
def placement_interface() -> None:
    """Method which allows for GET and POST requests.
    When a GET request is received, the method will render/return the placement.html template, 
    and assign the ships for the user and the size of the board.
    When a POST request is received, the method will retrieve the placement of the 
    users' ship and place them on the players board.
    It will also assign the AI's board with a random placement of battleships."""
    if request.method == "GET":
        return render_template('placement.html', ships = user_ships , board_size = len(user_board))
    if request.method == "POST":
        data = request.get_json()
        # Check to see if the data fetched from the json file matches the number of ships
        # that are available to place.
        if len(data) != len(user_ships):
            logging.error("Not all ships were placed by the user")
            raise ValueError("Not all ships that are within in the dictionary were placed.")
        else:
            try:
                with open('placement.json', 'w', encoding = "UTF-8") as file:
                    json.dump(data, file)
                players["Player_1"] = components.place_battleships(user_board, user_ships,"custom")
                players["AI_Player"] = components.place_battleships(ai_board, ai_ships, "random")
                return jsonify({'message': 'Received'}), 200
            except FileNotFoundError as fne:
                logging.error("The file that you are trying to write to does not exist.")
                raise FileNotFoundError("placement.json file not found.") from fne

@app.route(rule = "/", methods = ["GET"])
def root() -> None:
    """Method which allows for GET requests.
    When a GET request is received, the method will render/return the main.html template,
    and assign the board on the template with the players' board choice."""
    logging.info("The users' board was successfully processed.")
    return render_template('main.html', player_board = players["Player_1"])

@app.route(rule = "/attack", methods = ["GET"])
def process_attack() -> None:
    """Method which allows for GET requests.
    When a GET request is received, the method will retrieve the two x and y arguments
    for the players' desired attack location.
    These co-ordinates will be processed on the AI's board.
    An AI attack will also be generated and processed on the players' board.
    Logic is implemented to determine if the game should go on
    or a certain player has won the game."""
    if request.args:
        #Player's Guess/Turn
        x = request.args.get('x')
        y = request.args.get('y')
        user_attack = (x, y)
        player_attack_result = game_engine.attack((x,y), players["AI_Player"], ai_ships)
        # Check to see if an attack by the user has already been guessed
        while user_attack in previous_user_attacks:
            logging.warning("The user has clicked on the same sqaure more than once")
            return "Error - the user has clicked on the same sqaure more than once"
        previous_user_attacks.append(user_attack)

        ai_attack = mp_game_engine.generate_attack()
        # Check to see if an attack by the user has already been guessed
        while ai_attack in previous_ai_attacks:
            logging.warning("The AI has tried to guess on the same square as its previous attacks.")
            ai_attack = mp_game_engine.generate_attack()
        previous_ai_attacks.append(ai_attack)
        ai_attack_result = game_engine.attack(ai_attack, players["Player_1"], user_ships)

        game_won = False
        game_lost = False

        #Check to see if all ships have been sunken for either the AI or the user
        user_ships_sunk = all(value == 0 for value in user_ships.values())
        ai_ships_sunk = all(value == 0 for value in ai_ships.values())
        if ai_ships_sunk is True:
            game_won = True

        if user_ships_sunk is True:
            game_lost = True

        if game_won is True:
            logging.info("The game has ended and the user has won")
            return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack,
                             "finished":"Congratulations - You Won the Game!"})
        elif game_lost is True:
            logging.info("The game has ended and the user has won")
            return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack,
                            "finished":"Game Over! The AI sunk all your ships!"})
        else:
            logging.info("The AI attacked the users board and "
                         "the user has attacked the AI's board")
            if player_attack_result is True:
                logging.info("The player has hit the AI's ship!")
            else:
                logging.info("The player has missed the AI's ships")
            if ai_attack_result is True:
                logging.info("The AI has hit the player's ship!")
            else:
                logging.info("The AI has missed the player's ships")
            return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack})

# targeting_mode = False
# ai_next_hits = []
# ai_attack = None

# @app.route(rule = "/attack", methods = ["GET"])
# def process_attack_targeting_mode() -> None:
#     """Method which allows for GET requests.
#     When a GET request is received, the method will retrieve the two x and y arguments
#     for the players' desired attack location.
#     These co-ordinates will be processed on the AI's board.
#     An AI attack will also be generated and processed on the players' board.
#     Logic is implemented to determine if the game should go on
#     or a certain player has won the game."""
#     if request.args:
#         game_won = False
#         game_lost = False
#         global targeting_mode
#         global ai_next_hits
#         global ai_attack
#         ai_attack_result = None
#         type_of_ship_hit = None
#         #Player's Guess/Turn
#         x = request.args.get('x')
#         y = request.args.get('y')
#         user_attack = (x, y)
#         player_attack_result = game_engine.attack((x,y), players["AI_Player"], ai_ships)
#         # Check to see if an attack by the user has already been guessed
#         while user_attack in previous_user_attacks:
#             logging.warning("The user has clicked on the same sqaure more than once")
#             return "Error - the user has clicked on the same sqaure more than once"
#         previous_user_attacks.append(user_attack)

#         if ai_next_hits != []:
#             if targeting_mode is True:
#                 ai_attack = ai_next_hits[0]
#                 ai_next_hits.remove(ai_attack)
#                 ai_attack_result = game_engine.attack(ai_attack, players["Player_1"], user_ships)
#                 user_ships_sunk = all(value == 0 for value in user_ships.values())
#                 ai_ships_sunk = all(value == 0 for value in ai_ships.values())
#                 if ai_ships_sunk is True:
#                     game_won = True

#                 if user_ships_sunk is True:
#                     game_lost = True

#                 if game_won is True:
#                     logging.info("The game has ended and the user has won")
#                     return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack,
#                                 "finished":"Congratulations - You Won the Game!"})
#                 elif game_lost is True:
#                     logging.info("The game has ended and the user has won")
#                     return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack,
#                                 "finished":"Game Over! The AI sunk all your ships!"})
#                 else:
#                     logging.info("The AI attacked the users board and the "
#                                  "user has attacked the AI's board")
#                     if player_attack_result is True:
#                         logging.info("The player has hit the AI's ship!")
#                     else:
#                         logging.info("The player has missed the AI's ships")
#                     if ai_attack_result is True:
#                         logging.info("The AI has hit the player's ship!")
#                     else:
#                         logging.info("The AI has missed the player's ships")
#                     return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack})
#         else:
#             targeting_mode = False
#         if targeting_mode is False:
#             ai_attack = mp_game_engine.generate_attack()
#             # Check to see if an attack by the AI has already been guessed
#             while ai_attack in previous_ai_attacks:
#                 logging.warning("The AI has tried to guess on the "
#                                 "same square as its previous attacks.")
#                 ai_attack = mp_game_engine.generate_attack()
#             previous_ai_attacks.append(ai_attack)
#             ai_x, ai_y = ai_attack
#             type_of_ship_hit = user_board[int(ai_y)][int(ai_x)]
#             ai_attack_result = game_engine.attack(ai_attack, players["Player_1"], user_ships)
#             # Check to see if a hit was registered
#             if ai_attack_result is True:
#                 targeting_mode = True
#                 ai_next_hits = mp_game_engine.targeting_mode(ai_attack,players["Player_1"],
#                                                              type_of_ship_hit)
#                 for attack in ai_next_hits:
#                     previous_ai_attacks.append(attack)

#         # Check to see if all ships have been sunken by either AI or player
#         user_ships_sunk = all(value == 0 for value in user_ships.values())
#         ai_ships_sunk = all(value == 0 for value in ai_ships.values())
#         if ai_ships_sunk is True:
#             game_won = True

#         if user_ships_sunk is True:
#             game_lost = True

#         if game_won is True:
#             logging.info("The game has ended and the user has won")
#             return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack,
#                              "finished":"Congratulations - You Won the Game!"})
#         elif game_lost is True:
#             logging.info("The game has ended and the user has won")
#             return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack,
#                             "finished":"Game Over! The AI sunk all your ships!"})
#         else:
#             logging.info("The AI attacked the users board and the "
#                          "user has attacked the AI's board")
#             if player_attack_result is True:
#                 logging.info("The player has hit the AI's ship!")
#             else:
#                 logging.info("The player has missed the AI's ships")
#             if ai_attack_result is True:
#                 logging.info("The AI has hit the player's ship!")
#             else:
#                 logging.info("The AI has missed the player's ships")
#             return jsonify({"hit": player_attack_result, "AI_Turn": ai_attack})

if __name__ == '__main__':
    app.template_folder = "templates"
    app.run()
