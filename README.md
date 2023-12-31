# Self-Assessment

### General Completed Features
Every feature in the project specification has been completed and adhered to:
* A user an interact with the simple game loop which will be a one player game to guess battleships in the command-line.
* There is a multiplayer game loop, where a user can verse a simple AI opponent in a fun command-line game of battleships.
* A web based Battleships game with an AI opponent, using Flask.
* *Note that for the random algorithm, a method called check_ways_to_place has been created in components.py that will work in conjunction with the place_battleships method when the algorithm is set to "random".*
### Validation on Features
Defensive programming was utilized in order to solidify the integrity of the program:
* Input validation has been utilized throughout the project in order to make sure the game works properly, examples include type checks and range checks etc.
* Try and except statements were also used to make sure the user is interacting with the project in the correct way.

### Testing on Validation
Additional tests were created in the projects' directory under tests/test_by_student.py

### Logging
A log file has been created called battleships.log that stores logging events of the program.

## Additional Features Beyond Specification

### Strategic Placement of Ships
* A more sophisticated battleship placement algorithm has been implemented to add a harder difficulty level for the AI opponent.

#### How it works:
* I have added another algorithm to the place_battleships function called "strategic". The algorithm will choose a random pre-calculated placement configuration stored in the strategic_placements.json file and place the AI's ships according to that configuration.
* There are 20 different pre-calculated configurations based on these references: 
    * [https://www.instructables.com/How-to-Win-at-Battleship/#https://www.instructables.com/How-to-Win-at-Battleship/#]
    * [https://www.thesprucecrafts.com/how-to-win-at-battleship-411068#:~:text=Be%20asymmetrical%3A%20In%20other%20words,after%20finding%20the%20first%20one]
* The main talking points are to mostly place ships vertically as there is a natural tendancy to scan horizontally while a user is playing, to leave empty space between ships and avoiding the ships from touching.
* If you want to test it out, just change the algorithm of the AI's place_battleships function in mp_game_engine.py or main.py to "strategic".

### Keeping Track of Previous AI and User Attacks
* Lists are created for every time a game is run (in game_engine.py, mp_game_engine.py or main.py) and keeps track of previous user attacks and AI attacks in order to:
    * Make sure that the AI or the user won't guess the same location twice.
    * Add defensive programming to the main.py web based game, so that even if a user clicks on a already hit ship square, nothing will happen.

### Extremely Hard AI Mode (Targeting Mode)

* An extra method called targeting_mode was made in mp_game_engine.py 
* An extra method called process_attack_targeting_mode was made in main.py
#### How it works:
* After it has been activated (steps on how to do that are in the Getting Started Tutorial section), once the AI generates an attack that hits a ship, the next attacks generated by the AI will sink the ship that it initially hit in consecutive turns.

# Battleships ReadMe

## Introduction

This project is a Battleships game constructed by the University of Exeter which can be played as either a single player command-line game, or a two player game against an AI opponent in the command-line or as a web based interface game with a grid that a player can interact with to try beat an AI opponent. The user can either verse a normal AI opponent that will randomly place their ships and guess random co-ordinates, or can increase the difficulty by using targeting mode and "strategic" placement algorithm for the AI. The user and the AI will take alternative turns to try and sink all of the ships in the opponents' board.

## Prerequisites

#### The Python packages required to run this are:
Python version 3.11.5 <br>
blinker==1.7.0 <br>
click==8.1.7 <br>
Flask==3.0.0 <br>
iniconfig==2.0.0 <br>
itsdangerous==2.1.2 <br>
Jinja2==3.1.2 <br>
MarkupSafe==2.1.3 <br>
packaging==23.2 <br>
pluggy==1.3.0 <br>
pytest==7.4.3 <br>
Werkzeug==3.0.1 <br>


These can also be seen in a file called requirements.txt

#### The files required to run the program:
* The battleships.txt file should have a list of the ships that will be used for the game. 
They should be written in the format:
**ship_name,length_of_ship**.
The name of the ship should also be one word.
The typical (and recommended for this project) types of ships include:
    * Aircraft Carrier (5 Spaces)
    * Battleship (4 Spaces)
    * Cruiser (3 Spaces)
    * Submarine (3 Spaces)
    * Destroyer (2 Spaces)

* The placement.json file should store each ships placement, seperated by a comma:
    * **{ship_name:[startX_Coordinate, startY_Coordinate, orientation], etc.}**

* The strategic_placements.json file should be formatted the same, just seperating each configuration by curly brackets.

## Installation

The user could either install all of the required dependencies by:
`pip install -r requirements.txt` when in the root directory.

The user could also individually install each one by
`pip install pytest` ... for each one.

## Getting Started Tutorial
### For Simple One Player Command-Line Game
1. You must install all dependencies and required packages in requirements.txt
2. Open terminal in projects' directory and run **python3 game_engine.py** (the game_engine module).
3. You must enter co-ordinates in the format prompted to you using CLI to play the game and try to guess ships, where x is the column and y is the row on the board.
4. Once you have sunk all the ships, the game will terminate.
### For Multiplayer Command-Line Game  
1. You must install all dependencies and required packages in requirements.txt
2. You can go into the battleships.txt file and change the lengths of the ships, or names or add different ships, however it is recommended to use the standard ships in the battleships.txt file as that is normally how battleships is played.
3. Futhermore you can go into the placement.json file and change the orientation of your ships if need be.
The format you will need to follow is:
**{ship_name:[startX_Coordinate, startY_Coordinate, orientation], etc.}**
    * Ensure that the name of the ships in the placement.json file match the names in the battleships.txt file.
    * Also ensure that the ships are not generating outside of the boards' bounds.
4. Finally, you can choose between versing an AI opponent who will randomly place their ships, or choose a harder opponent by choosing an AI opponent that will place their ships based on pre-calculated ship placements. This can be done by choosing between "random" and "strategic" for the algorithm variable in the players dictionary where players is **players{"AI_Player"}**.

*Note that the strategic placement algorithm is based on the original five battleships in battleships.txt and will not update to changed ships in the file.*

5. Once you have chosen your ships their orientation, and the AI's placement algorithm, open the terminal in the projects' directory and run **python3 mp_game_engine.py** (the mp_game_engine module).

6. Interact with the CLI and input your guess with corresponding x and y co-ordinates that will be processed on the AI's board.

7. The game will terminate once you have sunken all of the AI's ships or in return the game will also terminate if the AI sinks all of your ships.

### For GUI Web-Based Interface Multiplater Game
1. You must install all dependencies and required packages in requirements.txt

2. You can go into the battleships.txt file and change the lengths of the ships, or names or add different ships, however it is recommended to use the standard ships in the battleships.txt file as that is normally how battleships is played.

3. Finally, you can choose between versing an AI opponent who will randomly place their ships, or choose a harder opponent by choosing an AI opponent that will place their ships based on pre-calculated ship placements. This can be done by choosing between "random" and "strategic" for the algorithm variable in the players dictionary where players is **players{"AI_Player"}**.

4. Once the AI's placement algorithm has been chosen, open the terminal in the projects' directory and run **python3 main.py** (the main.py module).

5. Open up your web-browser and at this URL: **127.0.0.1:5000/placement**

6. Use the grid provided on the browser to choose the placement of your ships.

7. Once you have placed all your ships, hit the "Send Game" button to send your board's layout through.

8. This will redirect you to another URL where you will guess sqaures (co-ordinates) on the AI's board. Turns will alternate between you and the AI player.

9. The game will terminate once either all of your ships or all of the AI's ships are sunken.

*NOTE - if you want to play against the extreme mode version of the AI's hits, in the **main.py module**, uncomment everything from line 120 till line 234. This will uncomment the process_attack_targeting_mode method and the variables associated with it. 
You must also then comment out the process_attack function from line 58 to line 118, so that the game will not get confused between the two methods as they have the same URL request. This will activate the extreme targeting mode for the AI which can only be used in the web interface version of the game.*

## Testing

Tests made can be seen in the tests folder **/tests.** In this folder contains 4 testing files (`test_by_student.py`, `test_functionality.py`,`test_helper_functions.py` and `test_students.py`) with 3 configuration files (`battleships.txt`, `placement.json` and `strategic_placements.json`). Further included is a `__init__.py` so the tests folder can be recognized. The tests provided by the University are `test_functionality.py`,`test_helper_functions.py` and `test_students.py`. The tests written by myself can be found in `test_by_student.py` These tests have been added by  in order to test additional funcitonality. 

*NOTE - I had an error were I could run tests perfectly fine using the sidebar in VS Code, however when I try and run `pytest` in the command-line, it throws me an error. I have spoken to multiple TA's and apparently this is an editor issue.*

#### If The Command-Line Works
To run tests using the command-line, open up a terminal in the root directory for the project and enter `pytest`.
#### If the Sidebar Works
To run tests using the sidebar in VS code, click on the Testing icon (shaped like a flask) and select `pytest`. This should allow VS code to discover all of the tests and they can either be run individually or can be run on the whole test set.

## Developer Documentation

Documentation can be seen throughout the project, in each module with docstrings and the use of commenting being included within the code.

My Sphinx documentation can be found by opening `docs/_build/html/index.html` in my projects' folder.

*NOTE - I had issues generating the document so I moved things around in directories to get it to at least generate just the names of the modules, by placing all modules in a 'battleship' folder, then moved all modules back out into the main folder. I spoke to Matt and other TA's and no one could solve the issue, however I still have the generation of the index.html file to show you I've attempted to generate the document. <br> Commands I used to attempt to generate the document: <br> `cd docs` <br> `sphinx-quickstart` <br> `sphinx-apidoc -o . ..` between this and the next command, I altered the confy.py file to add the necessary extensions and uncommented the path and changed the parameter to .. <br> `make html`*

Logs of events taking place within the program can be viewed by opening the `battleships.log` file. This log file will store any significant processes from the program, including errors.

### The components.py Module
Module contains the key-core functions used to set up the components of the game for all versions of it, single player/multiplayer command-line and web-based.

### The game_engine.py Module
Module contains the functions that wil manage the 
game mechanics of the single player game, this will be used to play the simple version of the game with simple board placement.

### The mp_game_engine.py Module
Module contains the functions that wil manage the 
game mechanics of the multiplayer game with an AI Opponent. The players' ships are placed using the placement.json file and the AI's ships can be placed randomly or strategically with the strategic_placements.json file.

### The main.py Module
Module which is the main entry point for the project, it allows the user to play on a development server against the AI. A user can either version a normal AI opponent who will attack randomly, or use the process_attack_targeting_mode method to enable the extreme AI mode which is very much improved, it will find the rest of the ship once a hit is registered. 

## Details

This was a coursework for ECM1400, a first year first term module for Computer Science at the University of Exeter.

Author: N/A <br>
License: MIT License which can be found in the projects root directory under **/LICENSE/license.txt** <br>
Handle: lorenzo-meixieira
Link to GitHub Repo: [https://github.com/lorenzo-meixieira/ECM1400_Coursework]
