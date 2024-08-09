import os
from collections import namedtuple

import pygame
from typing import List, Optional, Tuple

from dungeon_adventure.config import FONT_PATH, RESOURCES_DIR
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.models.items import Item


class RoomItemsDisplay:
    # Constants for sizing and positioning
    DISPLAY_WIDTH_FACTOR: float = 80
    DISPLAY_HEIGHT_FACTOR: float = 80
    X_POS: int = 100
    Y_POS: int = 100
    TITLE_FONT_SIZE: int = 8
    LIST_FONT_SIZE: int = 8
    ITEM_HEIGHT_FACTOR: int = 20
    ITEM_HORIZONTAL_MARGIN: int = 5
    ITEM_VERTICAL_MARGIN: int = 2.5
    ITEM_WIDTH_REDUCTION: int = 30
    ITEM_HEIGHT_REDUCTION: int = 60
    Position = namedtuple("Position", ["x", "y"])
    Size = namedtuple("Size", ["width", "height"])

    # Colors
    BACKGROUND_COLOR: Tuple[int, int, int, int] = (61, 32, 43, 60)  # RGBA
    TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # White
    ITEM_BACKGROUND_COLOR: Tuple[int, int, int, int] = (100, 100, 100, 128)  # RGBA

    def __init__(self, scale_factor: int):
        self.scale_factor: int = scale_factor

        self.display_size = self.calc_display_size(scale_factor)
        self.display_pos = self.calc_display_pos(scale_factor)
        self.display_rect = self.create_main_display_rect(scale_factor)

        self.title_font: pygame.font.Font = pygame.font.Font(
            FONT_PATH + "foldit.ttf", self.TITLE_FONT_SIZE * scale_factor
        )
        self.list_font: pygame.font.Font = pygame.font.Font(
            None, self.LIST_FONT_SIZE * scale_factor
        )
        self.item_height: int = self.ITEM_HEIGHT_FACTOR * scale_factor
        self.items: List[Item] = []

        # Create a transparent surface for the background
        self.display_background: pygame.Surface = pygame.Surface(
            (self.display_rect.width, self.display_rect.height), pygame.SRCALPHA
        )
        self.display_background.fill(self.BACKGROUND_COLOR)

    def calc_display_size(self, scale_factor: int) -> Size:
        display_width: int = int(self.DISPLAY_WIDTH_FACTOR * scale_factor)
        display_height: int = int(self.DISPLAY_HEIGHT_FACTOR * scale_factor)
        return self.Size(display_width, display_height)

    def calc_display_pos(self, scale_factor: int) -> Position:
        display_pos_x: int = self.X_POS * scale_factor
        display_pos_y: int = self.Y_POS * scale_factor
        return self.Position(display_pos_x, display_pos_y)

    def create_main_display_rect(self, scale_factor: int) -> pygame.Rect:
        display_rect: pygame.Rect = pygame.Rect(
            self.display_pos.x,
            self.display_pos.y,
            self.display_size.width,  # width of the display rectangle
            self.display_size.height - 60,  # height of the display rectangle
        )
        return display_rect

    def update(self, room: Room) -> None:
        """Update the list of items based on the current room."""
        self.items = room.items

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the room items display on the given surface."""
        # Draw transparent background
        surface.blit(
            self.display_background, self.display_rect
        )  # draw background at display rect
        # Draw border
        pygame.draw.rect(surface, (200, 200, 200), self.display_rect, 2)

        # Draw title
        title_surface: pygame.Surface = self.title_font.render(
            "Room Items", True, self.TEXT_COLOR
        )
        text_rect = title_surface.get_rect()
        text_rect.midtop = self.display_rect.midtop
        text_rect.y = text_rect.y + 10
        surface.blit(title_surface, text_rect)

        # Draw items
        for i, item in enumerate(self.items):
            item_background_rect = pygame.Rect(
                self.display_rect.x + (self.ITEM_HORIZONTAL_MARGIN * self.scale_factor),
                self.display_rect.y + ((i + 1) * self.item_height),
                self.display_size.width - self.ITEM_WIDTH_REDUCTION,
                self.item_height - 30,
            )

            # Create a transparent surface for each item background
            item_background: pygame.Surface = pygame.Surface(
                (item_background_rect.width, item_background_rect.height),
                pygame.SRCALPHA,
            )

            item_background.fill(self.ITEM_BACKGROUND_COLOR)

            surface.blit(item_background, item_background_rect)

            item_text_surface: pygame.Surface = self.list_font.render(
                item.name, True, self.TEXT_COLOR
            )

            surface.blit(
                item_text_surface,
                (
                    item_background_rect.x
                    + (self.ITEM_HORIZONTAL_MARGIN * self.scale_factor),
                    item_background_rect.y
                    + (self.ITEM_VERTICAL_MARGIN * self.scale_factor),
                ),
            )

    def get_item_at_position(self, pos: Tuple[int, int]) -> Optional[Item]:
        """Return the item at the given position, if any."""
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(
                self.display_rect.x + (self.ITEM_HORIZONTAL_MARGIN * self.scale_factor),
                self.display_rect.y + ((i + 1) * self.item_height),
                self.display_size.width
                - (self.ITEM_WIDTH_REDUCTION * self.scale_factor),
                self.item_height - (self.ITEM_HEIGHT_REDUCTION * self.scale_factor),
            )
            if item_rect.collidepoint(pos):
                return item
        return None

    def debug_rect(self, rect, name="Rectangle"):
        print(f"{name}:")
        print(f"  Position: ({rect.x}, {rect.y})")
        print(f"  Size: {rect.size}")
        print(f"  Width: {rect.width}, Height: {rect.height}")
        print(f"  Top-left: {rect.topleft}, Bottom-right: {rect.bottomright}")
        print(f"  Center: {rect.center}")
