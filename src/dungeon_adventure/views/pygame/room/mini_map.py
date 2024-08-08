from typing import Dict, Tuple

import pygame

from dungeon_adventure.enums.room_types import Direction
from dungeon_adventure.views.pygame.room.game_room import GameRoom


class MiniMap:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.minimap_size = (250, 250)  # Adjust as needed
        self.room_size = (60, 60)  # Size of each room on the minimap
        self.minimap_surface = pygame.Surface(self.minimap_size)
        self.minimap_rect = pygame.Rect(
            screen_width - self.minimap_size[0] - 10,
            10,
            *self.minimap_size
        )
        self.room_images: Dict[str, pygame.Surface] = {}

    def update(self, current_room: GameRoom, all_rooms: Dict[str, GameRoom]):
        self.minimap_surface.fill((50, 50, 50))  # Dark gray background

        # Get adjacent rooms
        adjacent_rooms = self._get_adjacent_rooms(current_room, all_rooms)

        # Draw rooms on minimap
        center_pos = (self.minimap_size[0] // 2, self.minimap_size[1] // 2)
        self._draw_room(current_room, center_pos, True)

        for direction, room in adjacent_rooms.items():
            if room:
                pos = self._get_adjacent_position(center_pos, direction)
                self._draw_room(room, pos)

    def _get_adjacent_rooms(self, current_room: GameRoom, all_rooms: Dict[str, GameRoom]) -> Dict[Direction, GameRoom]:
        adjacent_rooms = {}
        for direction in Direction:
            connected_room = current_room.room.connections.get(direction)
            if connected_room:
                adjacent_rooms[direction] = all_rooms[connected_room.name]
            else:
                adjacent_rooms[direction] = None
        return adjacent_rooms

    def _get_adjacent_position(self, center_pos: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
        x, y = center_pos
        if direction == Direction.NORTH:
            return (x, y - self.room_size[1])
        elif direction == Direction.SOUTH:
            return (x, y + self.room_size[1])
        elif direction == Direction.WEST:
            return (x - self.room_size[0], y)
        elif direction == Direction.EAST:
            return (x + self.room_size[0], y)

    def _draw_room(self, room: GameRoom, position: Tuple[int, int], is_current: bool = False):
        if room.room.name not in self.room_images:
            self.room_images[room.room.name] = pygame.transform.scale(room.image, self.room_size)

        room_image = self.room_images[room.room.name]
        rect = room_image.get_rect(center=position)
        self.minimap_surface.blit(room_image, rect)

        if is_current:
            pygame.draw.rect(self.minimap_surface, (255, 0, 0), rect, 2)  # Red outline for current room

    def draw(self, screen: pygame.Surface):
        screen.blit(self.minimap_surface, self.minimap_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.minimap_rect, 2)  # White border