from src.enums.room_types import Direction


class PlayerActionController:
    def __init__(self, game_model):
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
            player.add_item_to_inventory(item)
            return True
        return False

    # and we can add other player actions like use_item or attack etc
