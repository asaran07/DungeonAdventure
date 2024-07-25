from src.dungeon import Room
from src.enums.room_types import Direction
from src.game.dungeon_adventure import GameModel


class PlayerActionController:
    """
    Serves as the bridge between user inputs and game state changes. This class contains methods for all possible
    player actions (e.g., moving, picking up items, using items, attacking) and is responsible for validating these
    actions and updating the game state accordingly. It works with GameModel ensuring all player actions
    are consistent with the game's rules and current state.
    """

    def __init__(self, game_model: GameModel):
        self.game_model = game_model

    def move_player(self, direction: Direction):
        player = self.game_model.player
        current_room = player.current_room

        if direction in dict(current_room.get_open_gates()):
            new_room = current_room.connections[direction]
            player.current_room = new_room
            return True
        return False

    def pick_up_item(self, item):
        player = self.game_model.player
        if item in player.current_room.items:
            player.current_room.remove_item(item)
            player.add_item_to_player_inventory(item)
            return True
        return False

    # and we can add other player actions like use_item or attack etc
    def handle_action(self, action):
        pass
