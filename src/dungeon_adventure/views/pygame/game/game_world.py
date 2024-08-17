import logging
from typing import Dict, Optional

import pygame

from dungeon_adventure.enums.game_state import GameState
from dungeon_adventure.enums.item_types import ItemType, PillarType
from dungeon_adventure.enums.room_types import Direction, RoomType
from dungeon_adventure.game_model import GameModel
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.views.pygame.room.game_room import GameRoom
from dungeon_adventure.views.pygame.sprites.composite_player import CompositePlayer
from serialization.game_snapshot import GameSnapshotPygame, save_game, load_game


class GameWorld:
    def __init__(self, game_model: GameModel, composite_player: CompositePlayer):
        self.dungeon = game_model.dungeon
        self.game_rooms = pygame.sprite.Group()
        self.room_dict: Dict[str, GameRoom] = {}
        self.current_room: Optional[GameRoom] = None
        self.composite_player = composite_player
        self.player_sprite = pygame.sprite.GroupSingle()
        self._game_model = game_model
        self.on_combat_initiated = None
        self.on_items_in_room = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initializing GameWorld")
        self.pit_encounter = None
        self.on_room_enter = None
        self.on_win_condition = None
        self.on_combat_end = None

    @property
    def game_model(self):
        return self._game_model

    @game_model.setter
    def game_model(self, value):
        self._game_model = value

    def initialize(self):
        self._create_game_rooms()
        self.current_room = self._get_starting_room()
        self.current_room.room.is_visible = True
        self.composite_player.initialize()
        self.composite_player.py_player.rect.center = self.current_room.rect.center
        self.player_sprite.add(self.composite_player.py_player)

    def _create_game_rooms(self):
        for room_name, room in self.dungeon.rooms.items():
            game_room = GameRoom(room)
            self.room_dict[room_name] = game_room
            self.game_rooms.add(game_room)

        # Initialize and position rooms after all have been created
        for game_room in self.room_dict.values():
            game_room.initialize()
            game_room.set_position((480 // 2, 270 // 2))

    def _get_starting_room(self) -> GameRoom:
        starting_room_name = next(iter(self.dungeon.rooms.keys()))
        return self.room_dict[starting_room_name]

    def handle_save(self):
        # room_dict_values = []
        # for item in self.room_dict.values():
        #     room_dict_values.append(item.room)
        proj_state = GameSnapshotPygame(
            self.dungeon,
            # room_dict_values,
            self.current_room.room,
            self.composite_player.player,
            self._game_model,
        )
        save_game(proj_state, "save.pkl")
        self.logger.info("Saving Game")

    def handle_load(self):
        try:
            # TODO: Get rid of unnecessary logger stuff and comments
            proj_state: GameSnapshotPygame = load_game("save.pkl")
            self.dungeon = proj_state.get_dungeon()
            self.logger.info("test")
            strang = ("room_dict:", self.room_dict)
            self.logger.info(strang)
            other_strang = ("room_dict:", self.room_dict)
            # self.room_dict = proj_state.get_room_dict()
            # self.room_dict.values() = proj_state.get_room_dict_values()
            # for key, new_value in zip(self.room_dict.keys(), proj_state.get_room_dict_values()):
            #     self.room_dict[key].room = new_value
            other_strang = ("room_dict:", self.room_dict)
            self.logger.info(other_strang)
            self.current_room.room = proj_state.get_current_room()
            self.current_room.initialize()
            self.composite_player.player = proj_state.get_player()
            # self.composite_player.initialize()
            self.game_model = proj_state.get_game_model()

            self.logger.info("Loading Game")
        except FileNotFoundError as e:
            #  display message saying file wasn't found here, get rid of print statement
            # use player_message_display (I think) once it's finished
            print(e)
        # try:
        #     proj_state: GameSnapshotPygame = load_game("save.pkl")
        #     self.dungeon = proj_state.get_dungeon()
        #     self.current_room = self.room_dict[proj_state.get_current_room().name]
        #     self.current_room.initialize()  # Reinitialize visuals for the current room
        #     self.composite_player.player = proj_state.get_player()
        #     self.game_model = proj_state.get_game_model()
        #
        #     # Reinitialize player position in the room
        #     self.composite_player.py_player.rect.center = self.current_room.rect.center
        #
        #     # Update the minimap to reflect the current game state
        #     # self.update_minimap()
        #
        #     self.draw(pygame.display.get_surface())  # Force a visual refresh
        #
        #     self.logger.info("Loading Game")
        # except FileNotFoundError as e:
        #     print(e)

    def update(self, dt):
        self.composite_player.update(dt, self.current_room)
        self.game_rooms.update()
        self._check_room_transition()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the current game world state to the given surface.

        :param surface: The pygame surface to draw on
        """
        # Draw the current room
        self.current_room.draw(surface)

        # Draw the player
        self.player_sprite.draw(surface)

    def draw_debug(self, surface: pygame.Surface) -> None:
        """
        Draw debug information for the game world.

        :param surface: The pygame surface to draw on
        """
        # Draw room hitboxes
        self.current_room.draw_hitboxes(surface)

    def handle_take_item(self):
        item = self.current_room.room.items[0] if self.current_room.room.items else None
        if item:
            try:
                self.composite_player.inventory.add_item(item)
                self.current_room.room.remove_item(item)
                print(f"Took {item.name}")
            except Exception as e:
                print(f"Couldn't take {item.name}: {str(e)}")

    def handle_drop_item(self):
        # For simplicity, drop the last item in the inventory
        if self.composite_player.inventory._items:
            item_id, (item, quantity) = self.composite_player.inventory._items.popitem()
            self.current_room.room.add_item(item)
            print(f"Dropped {item.name}")
        else:
            print("No items to drop")

    def _check_room_transition(self):
        player_pos = self.composite_player.rect.center
        player_height = self.composite_player.rect.height
        door_direction = self.current_room.get_door_at_position(
            player_pos, player_height
        )
        if door_direction:
            self._handle_room_transition(door_direction)

    def _handle_room_transition(self, direction: Direction):
        self.logger.debug(
            f"Room transition: {self.current_room.room.name} -> {direction}"
        )
        self.current_room.room.is_visible = True
        current_dungeon_room = self.current_room.room
        next_dungeon_room = current_dungeon_room.connections[direction]
        if next_dungeon_room:
            next_room_name = next_dungeon_room.name
            self.current_room = self.room_dict[next_room_name]
            self.composite_player.current_room = next_room_name
            self._reposition_player(direction)
            self._handle_room_encounters()

    def _handle_room_encounters(self):
        if self.current_room.room.room_type is RoomType.PIT:
            self.composite_player.hurt(20)
            self.logger.info(f"Pit trap found in room: {self.current_room.room.name}")
            if self.pit_encounter:
                self.pit_encounter()
        if self.current_room.room.has_monsters:
            self.logger.info(f"Monsters found in room: {self.current_room.room.name}")
            self.logger.debug(
                f"Monsters: {[m.name for m in self.current_room.room.monsters]}"
            )
            self.logger.info("Setting GameState to IN_COMBAT")
            self.game_model.game_state = GameState.IN_COMBAT
            if self.on_combat_initiated:
                self.on_combat_initiated()
        if self.current_room.room:
            if self.on_room_enter:
                self.on_room_enter()
            if self.on_items_in_room:
                self.on_items_in_room()
            self._check_win_condition()
        else:
            self.logger.debug(f"Entered empty room: {self.current_room.room.name}")

    def _check_win_condition(self):
        if self.current_room.room.room_type is RoomType.EXIT:
            inventory_items = self.composite_player.inventory.get_all_items()
            pillar_types = set()

            for item, _ in inventory_items:
                if item.item_type == ItemType.PILLAR:
                    pillar_types.add(item.pillar_type)

            if len(pillar_types) == len(PillarType):
                self.logger.info(
                    "Player has collected all pillar types. Win condition met!"
                )
                if self.on_win_condition:
                    self.on_win_condition()

    def _reposition_player(self, entry_direction: Direction):
        opposite_direction = Room.opposite(entry_direction)
        door_hitbox = self.current_room.visuals.door_hitboxes[opposite_direction]

        # Get the room's center offset
        room_center_offset = self.current_room.visuals.get_center_offset()

        # Calculate the door's position relative to the room's center
        door_relative_pos = (
            door_hitbox.centerx + room_center_offset[0],
            door_hitbox.centery + room_center_offset[1],
        )

        # Set the player's position
        self.composite_player.rect.center = door_relative_pos

        # Adjust the player's position to be just inside the room
        if opposite_direction == Direction.NORTH:
            self.composite_player.rect.top = door_hitbox.bottom + room_center_offset[1]
        elif opposite_direction == Direction.SOUTH:
            self.composite_player.rect.bottom = door_hitbox.top + room_center_offset[1]
        elif opposite_direction == Direction.WEST:
            self.composite_player.rect.left = door_hitbox.right + room_center_offset[0]
        elif opposite_direction == Direction.EAST:
            self.composite_player.rect.right = door_hitbox.left + room_center_offset[0]

    def end_combat(self):
        if self.on_combat_end:
            self.on_combat_end()

    def on_game_over(self):
        self.game_model.game_state = GameState.GAME_OVER
        if self.on_win_condition:
            self.on_win_condition()


