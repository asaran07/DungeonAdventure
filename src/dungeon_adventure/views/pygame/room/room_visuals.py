import pygame
from dungeon_adventure.enums.room_types import Direction

class RoomVisuals:
    # Constants
    DEFAULT_ROOM_DIMENSIONS = (128, 80)
    DEFAULT_FLOOR_DIMENSIONS = (96, 48)
    FLOOR_RECT_POSITION = (16, 16)

    # Door positions relative to room (x, y, width, height)
    DOOR_POSITIONS = {
        Direction.NORTH: (48, 0, 30, 2),
        Direction.SOUTH: (48, 78, 30, 2),
        Direction.WEST: (9, 29, 2, 20),
        Direction.EAST: (116, 29, 2, 20)
    }

    # Extended floor areas relative to doors
    EXTENDED_FLOOR_OFFSETS = {
        Direction.NORTH: (0, 0, 0, 16),
        Direction.SOUTH: (0, -14, 0, 16),
        Direction.WEST: (0, 0, 8, 0),
        Direction.EAST: (-6, 0, 8, 0)
    }

    def __init__(self, image_path: str, screen_size: tuple):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen_size = screen_size
        self.rect = self.image.get_rect()
        self._walkable_floor_hitbox = pygame.Rect(
            *self.FLOOR_RECT_POSITION,
            *self.DEFAULT_FLOOR_DIMENSIONS
        )
        self.door_hitboxes = {}
        self.extended_floor_areas = {}

        # Debug colors
        self.floor_color = (128, 0, 128)  # Purple
        self.door_color = (255, 250, 0)  # Yellow
        self.extended_floor_color = (0, 0, 255)  # Blue

    @property
    def walkable_floor_hitbox(self):
        return self._walkable_floor_hitbox.move(self.get_center_offset())

    def get_center_offset(self):
        x = (self.screen_size[0] - self.DEFAULT_ROOM_DIMENSIONS[0]) // 2
        y = (self.screen_size[1] - self.DEFAULT_ROOM_DIMENSIONS[1]) // 2
        return (x, y)

    def create_hitboxes(self, open_directions):
        self.door_hitboxes.clear()
        self.extended_floor_areas.clear()

        # For each direction in open_directions we create a hitbox and extend the floor area.
        for direction in open_directions:
            self._create_door_hitbox(direction)
            self._extend_floor_area(direction)

    def _create_door_hitbox(self, direction: Direction):
        # Creates a pygame rectangle of a specific size and position according to self.DOOR_POSITIONS
        # and sets the specified direction in self.door_hitboxes to the newly created hitbox.
        self.door_hitboxes[direction] = pygame.Rect(self.DOOR_POSITIONS[direction])

    def _extend_floor_area(self, direction):
        door_rect = self.door_hitboxes[direction]
        offset = self.EXTENDED_FLOOR_OFFSETS[direction]
        extended_rect = pygame.Rect(
            door_rect.x + offset[0],
            door_rect.y + offset[1],
            door_rect.width + offset[2],
            door_rect.height + offset[3]
        )
        self.extended_floor_areas[direction] = extended_rect

    def draw_hitboxes(self, surface):
        center_offset = self.get_center_offset()

        # Draw main floor
        pygame.draw.rect(surface, self.floor_color, self.walkable_floor_hitbox, 2)

        # Draw doors and extended floor areas
        for hitbox in self.door_hitboxes.values():
            pygame.draw.rect(surface, self.door_color, hitbox.move(center_offset))

        for extended_area in self.extended_floor_areas.values():
            pygame.draw.rect(surface, self.extended_floor_color, extended_area.move(center_offset), 2)

    def get_full_floor_rect(self):
        full_rect = self.walkable_floor_hitbox.copy()
        center_offset = self.get_center_offset()
        for extended_area in self.extended_floor_areas.values():
            full_rect.union_ip(extended_area.move(center_offset))
        return full_rect

    def is_within_floor(self, point):
        return self.get_full_floor_rect().collidepoint(point)

    def get_door_at_position(self, pos):
        center_offset = self.get_center_offset()
        for direction, hitbox in self.door_hitboxes.items():
            if hitbox.move(center_offset).collidepoint(pos):
                return direction
        return None