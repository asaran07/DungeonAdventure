import pygame

from src.dungeon import Room
from src.enums import Direction


class PyRoom(pygame.sprite.Sprite):
    def __init__(self, image_path, room: Room):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.room = room

        floor_left = (128 - 96) // 2  # Centering the floor horizontally
        floor_top = (80 - 48) // 2  # Centering the floor vertically
        self._floor_rect = pygame.Rect(floor_left, floor_top, 96, 48)

        self.door_hitboxes = self._create_door_hitboxes()

    @property
    def floor_rect(self):
        # Return the floor rect adjusted for the room's position on the game surface
        x = (480 - 128) // 2
        y = (270 - 80) // 2
        return self._floor_rect.move(x, y)

    def is_within_floor(self, rect) -> bool:
        return self.floor_rect.contains(rect)

    def _create_door_hitboxes(self):
        door_hitboxes = {}
        door_width = 20
        door_height = 5

        for direction, connected_room in self.room.connections.items():
            if connected_room:
                if direction == Direction.NORTH:
                    hitbox = pygame.Rect(
                        self.floor_rect.centerx - door_width // 2,
                        self.floor_rect.top - door_height,
                        door_width,
                        door_height,
                    )
                elif direction == Direction.SOUTH:
                    hitbox = pygame.Rect(
                        self.floor_rect.centerx - door_width // 2,
                        self.floor_rect.bottom,
                        door_width,
                        door_height,
                    )
                elif direction == Direction.WEST:
                    hitbox = pygame.Rect(
                        self.floor_rect.left - door_height,
                        self.floor_rect.centery - door_width // 2,
                        door_height,
                        door_width,
                    )
                elif direction == Direction.EAST:
                    hitbox = pygame.Rect(
                        self.floor_rect.right,
                        self.floor_rect.centery - door_width // 2,
                        door_height,
                        door_width,
                    )
                door_hitboxes[direction] = hitbox

        return door_hitboxes

    def draw_hitboxes(self, surface):
        # Draw floor rectangle
        pygame.draw.rect(surface, (0, 0, 255), self.floor_rect, 2)  # Blue rectangle

        # Draw door hitboxes
        for direction, hitbox in self.door_hitboxes.items():
            pygame.draw.rect(
                surface, (255, 165, 0), hitbox, 2
            )  # Orange rectangles for doors

    def get_door_at_position(self, pos):
        for direction, hitbox in self.door_hitboxes.items():
            if hitbox.collidepoint(pos):
                return direction
        return None

    # def draw_floor_rect(self, surface):
    #     pygame.draw.rect(surface, (0, 0, 255), self.floor_rect, 2)  # Blue rectangle
    #     # Draw a yellow line at the top of the floor rect
    #     pygame.draw.line(
    #         surface, (255, 255, 0), self.floor_rect.topleft, self.floor_rect.topright, 2
    #     )
