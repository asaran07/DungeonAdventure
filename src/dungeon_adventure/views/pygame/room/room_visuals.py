import pygame
from dungeon_adventure.enums.room_types import Direction


class RoomVisuals:
    # Constants
    DEFAULT_ROOM_DIMENSIONS = (128, 80)
    DEFAULT_FLOOR_DIMENSIONS = (96, 48)
    FLOOR_RECT_POSITION = (16, 16)

    # Door positions relative to room (x, y, width, height)
    DOOR_POSITIONS = {
        Direction.NORTH: (48, 0, 30, 4),
        Direction.SOUTH: (48, 78, 30, 2),
        Direction.WEST: (9, 29, 2, 20),
        Direction.EAST: (116, 29, 2, 20),
    }

    # Extended floor areas relative to doors
    EXTENDED_FLOOR_OFFSETS = {
        Direction.NORTH: (0, 0, 0, 16),
        Direction.SOUTH: (0, -16, 0, 16),
        Direction.WEST: (0, 0, 8, 0),
        Direction.EAST: (-6, 0, 8, 0),
    }

    def __init__(self, image_path: str, screen_size: tuple):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.screen_size = screen_size
        self.rect = self.image.get_rect()
        self._walkable_floor_hitbox = pygame.Rect(
            *self.FLOOR_RECT_POSITION, *self.DEFAULT_FLOOR_DIMENSIONS
        )
        self.door_hitboxes = {}
        self.extended_floor_areas = {}

        # Debug colors
        self.extended_color = (128, 0, 128)  # Purple
        self.floor_color = (0, 255, 0)  # Green
        self.door_color = (255, 250, 0)  # Yellow
        self.extended_floor_color = (0, 0, 255)  # Blue

    @property
    def walkable_floor_hitbox(self):
        return self._walkable_floor_hitbox.move(self.get_center_offset())

    def get_center_offset(self):
        x = (self.screen_size[0] - self.DEFAULT_ROOM_DIMENSIONS[0]) // 2
        y = (self.screen_size[1] - self.DEFAULT_ROOM_DIMENSIONS[1]) // 2
        return x, y

    def create_hitboxes(self, open_directions):
        self.door_hitboxes.clear()
        self.extended_floor_areas.clear()

        # For each direction in open_directions we create a hitbox and extend the floor area.
        for direction in open_directions:
            self._create_door_hitbox(direction)
            self._create_extended_floor_area(direction)

    def _create_door_hitbox(self, direction: Direction) -> None:
        # Creates a pygame rectangle (door hitbox) of a specific size and position according to self.DOOR_POSITIONS
        # and sets the specified direction in self.door_hitboxes to the newly created hitbox.
        self.door_hitboxes[direction] = pygame.Rect(self.DOOR_POSITIONS[direction])

    def _create_extended_floor_area(self, direction: Direction) -> None:
        # Get the door_hitbox of a specified direction
        door_hitbox = self.door_hitboxes[direction]
        # Since the extended area will be right next to the door hitboxes, we can add a certain offset to the
        # door hitboxes to create our extended walkable area.
        offset = self.EXTENDED_FLOOR_OFFSETS[direction]
        extended_rect = pygame.Rect(
            # Add the offset to each element of the door hitbox to create our extended door hitbox element
            door_hitbox.x + offset[0],
            door_hitbox.y + offset[1],
            door_hitbox.width + offset[2],
            door_hitbox.height + offset[3],
        )
        # Then save that inside extended floor areas
        self.extended_floor_areas[direction] = extended_rect

    def draw_hitbox_debug_outlines(self, surface):
        center_offset = self.get_center_offset()

        # Draw main floor
        pygame.draw.rect(surface, self.floor_color, self.walkable_floor_hitbox, 1)

        # Draw extended floor
        # pygame.draw.rect(surface, self.extended_color, self.get_full_floor_area(), 1)

        # Draw doors and extended floor areas
        for hitbox in self.door_hitboxes.values():
            pygame.draw.rect(surface, self.door_color, hitbox.move(center_offset))

        for extended_area in self.extended_floor_areas.values():
            pygame.draw.rect(
                surface, self.extended_floor_color, extended_area.move(center_offset), 1
            )

    def get_full_floor_area(self):
        """Returns a list of rectangles representing the full floor area."""
        center_offset = self.get_center_offset()
        areas = [self._walkable_floor_hitbox.move(center_offset)]
        for extended_area in self.extended_floor_areas.values():
            areas.append(extended_area.move(center_offset))
        return areas

    def is_within_floor(self, point):
        """Check if a point is within any part of the floor area."""
        # Adjust the point based on the room's position on the screen
        center_offset = self.get_center_offset()
        adjusted_point = (point[0] - center_offset[0], point[1] - center_offset[1])

        # Check main floor area
        if self._walkable_floor_hitbox.collidepoint(adjusted_point):
            return True

        # Check extended floor areas
        for extended_area in self.extended_floor_areas.values():
            if extended_area.collidepoint(adjusted_point):
                return True

        return False

    def get_door_at_position(self, pos, player_height):
        center_offset = self.get_center_offset()
        adjusted_pos = (pos[0] - center_offset[0], pos[1] - center_offset[1])

        # Use the bottom of the player sprite for collision
        feet_pos = (adjusted_pos[0], adjusted_pos[1] + player_height // 2)

        for direction, hitbox in self.door_hitboxes.items():
            if hitbox.collidepoint(feet_pos):
                return direction
        return None
