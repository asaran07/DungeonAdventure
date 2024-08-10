from typing import Dict, Optional

import pygame

from dungeon_adventure.enums.room_types import Direction
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.views.pygame.room.game_room import GameRoom
from dungeon_adventure.views.pygame.sprites.composite_player import CompositePlayer
from src import GameModel


class GameWorld:
    def __init__(self, game_model: GameModel, composite_player: CompositePlayer):
        self.dungeon = game_model.dungeon
        self.game_rooms = pygame.sprite.Group()
        self.room_dict: Dict[str, GameRoom] = {}
        self.current_room: Optional[GameRoom] = None
        self.composite_player = composite_player
        self.player_sprite = pygame.sprite.GroupSingle()

    def initialize(self):
        self._create_game_rooms()
        self.current_room = self._get_starting_room()
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

    def _check_room_transition(self):
        player_pos = self.composite_player.rect.center
        player_height = self.composite_player.rect.height
        door_direction = self.current_room.get_door_at_position(
            player_pos, player_height
        )
        if door_direction:
            self._handle_room_transition(door_direction)

    def _handle_room_transition(self, direction: Direction):
        current_dungeon_room = self.current_room.room
        next_dungeon_room = current_dungeon_room.connections[direction]
        if next_dungeon_room:
            next_room_name = next_dungeon_room.name
            self.current_room = self.room_dict[next_room_name]
            self.composite_player.current_room = (
                next_room_name  # update the player's location as well
            )
            self._reposition_player(direction)

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
