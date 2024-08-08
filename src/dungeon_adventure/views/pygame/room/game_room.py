import pygame

from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.views.pygame.room.room_visuals import RoomVisuals


class GameRoom(pygame.sprite.Sprite):
    def __init__(self, room: Room, image_path: str):
        super().__init__()
        self.room = room
        self.visuals = RoomVisuals(image_path, (480, 270))
        self.image = self.visuals.image
        self.rect = self.image.get_rect()
        self._setup_hitboxes()

    def _setup_hitboxes(self):
        open_directions = [
            direction
            for direction, connected_room in self.room.connections.items()
            if connected_room
        ]
        self.visuals.create_hitboxes(open_directions)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_hitboxes(self, surface):
        self.visuals.draw_hitbox_debug_outlines(surface)

    def get_door_at_position(self, pos):
        return self.visuals.get_door_at_position(pos)

    def is_within_floor(self, point):
        return self.visuals.is_within_floor(point)

    def update(self):
        # This method can be used for any game logic updates specific to this room
        pass
