import os

import pygame

from dungeon_adventure.config import RESOURCES_DIR
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.views.pygame.room.room_image_manager import RoomImageManager
from dungeon_adventure.views.pygame.room.room_visuals import RoomVisuals


class GameRoom(pygame.sprite.Sprite):
    def __init__(self, room: Room):
        super().__init__()
        self.room = room
        self.image_manager = RoomImageManager(
            os.path.join(RESOURCES_DIR, "room_images")
        )
        self._setup_room_image()
        self.visuals = RoomVisuals(self.image_path, (480, 270))
        self.image = self.visuals.image
        self.rect = self.image.get_rect()
        self._setup_hitboxes()

    def _setup_room_image(self):
        open_doors = [
            direction
            for direction, connected_room in self.room.connections.items()
            if connected_room
        ]
        self.image_path = self.image_manager.get_room_image(open_doors)

    def _setup_hitboxes(self):
        open_directions = [
            direction
            for direction, connected_room in self.room.connections.items()
            if connected_room
        ]
        self.visuals.create_hitboxes(open_directions)

    # def _setup_hitboxes(self):
    #     open_directions = [
    #         direction
    #         for direction, connected_room in self.room.connections.items()
    #         if connected_room
    #     ]
    #     self.visuals.create_hitboxes(open_directions)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_hitboxes(self, surface):
        self.visuals.draw_hitbox_debug_outlines(surface)

    def get_door_at_position(self, pos, player_height):
        return self.visuals.get_door_at_position(pos, player_height)

    def is_within_floor(self, point):
        return self.visuals.is_within_floor(point)

    def update(self):
        # This method can be used for any game logic updates specific to this room
        pass
