# Moskovskiy.chess
Very good chess by greatest Kirill Moskovskiy TRPO24-1
# Chess and Checkers Simulator: Object-Oriented Version

This project is a console application implemented in Python that allows you to play both chess and checkers. The program features advanced functionalities such as move history with undo/redo, hints for possible moves, threat analysis, and the ability to save and load games. Additionally, it supports unique chess pieces such as the Wizard, Dragon, and Archer.

## Repository Contents

- **chesss.py** – The main code file containing the implementation of the game logic, board, pieces, and gameplay.
- **documentation.txt** – Detailed documentation of the project.
- **requirements.txt** – List of dependencies (none; only the standard Python libraries are used).
- **README.md** – This file.

## Project Description

### Core Functionality

- **Chess Mode:**  
  Standard chess game on an 8x8 board. Players input moves in standard chess notation (e.g., `e2 e4`), and the program validates moves according to chess rules.
  
- **Checkers Mode:**  
  The game supports checkers via the same board (using the `game_type` parameter) with dedicated rules for regular checkers and kings.
  
- **Move History:**  
  All moves are tracked, allowing you to undo (`back`) and redo (`next`) moves.
  
- **Hints:**  
  The command `hint <position>` (e.g., `hint e2`) displays all possible moves for a piece on a given square with visual highlighting.
  
- **Threat Analysis:**  
  The command `threats <position>` (e.g., `threats e4`) shows which opponent pieces threaten the square.
  
- **Saving/Loading:**  
  Save the game using `save <filename>` and load a game using `load <filename>`.

### Additional Features

- **Unique Chess Pieces:**
  - **Wizard (w/W):** Combines moves of a knight and a king.
  - **Dragon (d/D):** Combines moves of a rook and a knight.
  - **Archer (a/A):** Moves like a bishop or "shoots" diagonally two squares, attacking opponent pieces.

- **Checkers Pieces:**
  - **Checker (b/W):** Moves diagonally forward and captures by jumping.
  - **KingChecker (k/K):** Moves diagonally in any direction and captures by jumping.

## Installation and Running

### Requirements

- Python 3.6 or higher.
- No external libraries are required; the game uses only the standard Python library.

### How to Run the Game

1. Clone or download the repository.
2. Open a terminal in the repository directory.
3. Run the game using the command:

   ```bash
   python chesss.py
When prompted, select the game mode:

Enter 1 to play Chess.

Enter 2 to play Checkers.

Follow the on-screen instructions. Examples of commands include:

Move: e2 e4

Undo Move: back

Redo Move: next

Hint: hint e2

Threats: threats e4

Save Game: save game.txt

Load Game: load game.txt

Exit: exit
