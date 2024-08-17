import os
from typing import Dict, Tuple

import pygame

from dungeon_adventure.config import RESOURCES_DIR
from dungeon_adventure.enums.item_types import ItemType
from dungeon_adventure.enums.room_types import Direction, RoomType
from dungeon_adventure.views.pygame.room.game_room import GameRoom


class MiniMap:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.minimap_size = (250, 250)  # Adjust as needed
        self.room_size = (70, 70)  # Size of each room on the minimap
        self.minimap_surface = pygame.Surface(self.minimap_size)
        self.minimap_rect = pygame.Rect(
            screen_width - self.minimap_size[0] - 10, 10, *self.minimap_size
        )
        self.room_images: Dict[str, pygame.Surface] = {}
        # Load and scale icon images
        icon_size = (30, 30)
        self.chest_icon = pygame.transform.scale(
            pygame.image.load(
                os.path.join(RESOURCES_DIR, "icons", "chest.png")
            ).convert_alpha(),
            icon_size,
        )
        self.pillar_icon = pygame.transform.scale(
            pygame.image.load(
                os.path.join(RESOURCES_DIR, "icons", "pillar.png")
            ).convert_alpha(),
            icon_size,
        )
        self.exit_icon = pygame.transform.scale(
            pygame.image.load(
                os.path.join(RESOURCES_DIR, "icons", "banner.png")
            ).convert_alpha(),
            icon_size,
        )
        self.entrance_icon = pygame.transform.scale(
            pygame.image.load(
                os.path.join(RESOURCES_DIR, "icons", "banner_green.png")
            ).convert_alpha(),
            icon_size,
        )
        self.vision_potion_active = False

    def activate_vision_potion(self):
        print("Activating vision potion")
        self.vision_potion_active = True

    def deactivate_vision_potion(self):
        self.vision_potion_active = False

    def update(self, current_room: GameRoom, all_rooms: Dict[str, GameRoom]):
        self.minimap_surface.fill((26, 12, 17))  # Dark gray background

        # Get adjacent rooms
        adjacent_rooms = self._get_adjacent_rooms(current_room, all_rooms)

        # Draw rooms on minimap
        center_pos = (self.minimap_size[0] // 2, self.minimap_size[1] // 2)
        self._draw_room(current_room, center_pos, True)

        for direction, room in adjacent_rooms.items():
            if not self.vision_potion_active:
                if room and room.room.is_visible:  # Only draw visible rooms
                    pos = self._get_adjacent_position(center_pos, direction)
                    self._draw_room(room, pos)
            else:
                if room:
                    pos = self._get_adjacent_position(center_pos, direction)
                    self._draw_room(room, pos)

    def _get_adjacent_rooms(
        self, current_room: GameRoom, all_rooms: Dict[str, GameRoom]
    ) -> Dict[Direction, GameRoom]:
        adjacent_rooms = {}
        for direction in Direction:
            connected_room = current_room.room.connections.get(direction)
            if connected_room:
                adjacent_rooms[direction] = all_rooms[connected_room.name]
            else:
                adjacent_rooms[direction] = None
        return adjacent_rooms

    def _get_adjacent_position(
        self, center_pos: Tuple[int, int], direction: Direction
    ) -> Tuple[int, int]:
        x, y = center_pos
        if direction == Direction.NORTH:
            return (x, y - self.room_size[1])
        elif direction == Direction.SOUTH:
            return (x, y + self.room_size[1])
        elif direction == Direction.WEST:
            return (x - self.room_size[0], y)
        elif direction == Direction.EAST:
            return (x + self.room_size[0], y)

    def _draw_room(
        self, room: GameRoom, position: Tuple[int, int], is_current: bool = False
    ):
        if room.room.name not in self.room_images:
            self.room_images[room.room.name] = pygame.transform.scale(
                room.image, self.room_size
            )

        room_image = self.room_images[room.room.name]
        rect = room_image.get_rect(center=position)
        self.minimap_surface.blit(room_image, rect)

        if is_current:
            pygame.draw.rect(
                self.minimap_surface, (255, 0, 0), rect, 2
            )  # Red outline for current room

        self._draw_item_icon(room, rect)
        self._draw_pillar_icon(room, rect)
        self._draw_exit_icon(room, rect)
        self._draw_entrance_icon(room, rect)

    def _draw_item_icon(self, room: GameRoom, room_rect: pygame.Rect):
        if room.room.items:
            icon_pos = (
                room_rect.right - 5 - self.chest_icon.get_width(),
                room_rect.bottom - 5 - self.chest_icon.get_height(),
            )
            self.minimap_surface.blit(self.chest_icon, icon_pos)

    def _draw_pillar_icon(self, room: GameRoom, room_rect: pygame.Rect):
        if any(item.item_type == ItemType.PILLAR for item in room.room.items):
            icon_pos = (
                room_rect.left + 5,
                room_rect.bottom - 5 - self.pillar_icon.get_height(),
            )
            self.minimap_surface.blit(self.pillar_icon, icon_pos)

    def _draw_exit_icon(self, room: GameRoom, room_rect: pygame.Rect):
        if room.room.room_type == RoomType.EXIT:
            icon_pos = (
                room_rect.right - 5 - self.exit_icon.get_width(),
                room_rect.bottom - 5 - self.exit_icon.get_height(),
            )
            self.minimap_surface.blit(self.exit_icon, icon_pos)

    def _draw_entrance_icon(self, room: GameRoom, room_rect: pygame.Rect):
        if room.room.room_type == RoomType.ENTRANCE:
            icon_pos = (
                room_rect.right - 5 - self.entrance_icon.get_width(),
                room_rect.bottom - 5 - self.entrance_icon.get_height(),
            )
            self.minimap_surface.blit(self.entrance_icon, icon_pos)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.minimap_surface, self.minimap_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.minimap_rect, 2)  # White border
