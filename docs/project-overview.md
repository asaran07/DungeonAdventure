# Project Overview

## High-Level Architecture

Dungeon Adventure is structured using the Model-View-Controller (MVC) pattern:

- Model: `GameModel` in `dungeon_adventure.py`
- View: `ConsoleView` in `console_view.py`
- Controller: `GameController` in `game_controller.py`

## Module Dependencies

- `characters`: Contains `DungeonCharacter`, `Hero`, and `Monster` classes
- `dungeon`: Manages `Dungeon` and `Room` classes
- `items`: Defines various item types (weapons, potions, etc.)
- `enums`: Contains game-related enumerations
- `controllers`: Handles game logic and player actions
- `views`: Manages game display and user input

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`
4. Start the game: `python src/main.py`
