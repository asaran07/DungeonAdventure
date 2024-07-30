# Game Flow

## Main Game Loop

The main game loop is managed by the `GameController` class in `src/controllers/game_controller.py`.

1. Initialize game state (TITLE_SCREEN)
2. While game is not over:
   - Handle current game state
   - Process player input
   - Update game state
3. End game

## State Transitions

Game states are defined in `src/enums/game_state.py`:

- TITLE_SCREEN
- PLAYER_CREATION
- EXPLORING
- COMBAT
- INVENTORY
- GAME_OVER

The `GameController` manages transitions between these states based on player actions and game events.

## Player Action Handling

Player actions are processed by the `PlayerActionController` class in `src/controllers/player_action_controller.py`.

Key methods:

- `handle_action(action: str)`: Interprets and executes player commands
- `move_player(direction: Direction) -> bool`: Moves the player to a new room
- `pick_up_item(item: Item) -> bool`: Adds an item to the player's inventory

The `GameController` delegates player input to the `PlayerActionController` for processing.
