from collections import namedtuple
from typing import List, Optional, Tuple

import pygame

from dungeon_adventure.config import FONT_PATH
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.models.items import Item


class RoomItemsDisplay:
    # Constants for sizing and positioning
    DISPLAY_WIDTH_FACTOR: float = 80
    DISPLAY_HEIGHT_FACTOR: float = 80
    X_POS: int = 100
    Y_POS: int = 100
    TITLE_FONT_SIZE: int = 24
    LIST_FONT_SIZE: int = 20
    ITEM_HEIGHT_FACTOR: int = 20
    ITEM_HORIZONTAL_MARGIN: int = 5
    ITEM_WIDTH_REDUCTION: int = 30
    ITEM_HEIGHT_REDUCTION: int = 60
    Position = namedtuple("Position", ["x", "y"])
    Size = namedtuple("Size", ["width", "height"])

    # Colors
    BACKGROUND_COLOR: Tuple[int, int, int, int] = (50, 50, 50, 60)  # RGBA
    TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # White
    ITEM_BACKGROUND_COLOR: Tuple[int, int, int, int] = (100, 100, 100, 128)  # RGBA

    def __init__(self, scale_factor: int):
        self.scale_factor: int = scale_factor

        self.display_size = self.calc_display_size(scale_factor)
        self.display_pos = self.calc_display_pos(scale_factor)
        self.display_rect = self.create_main_display_rect()

        self.title_font: pygame.font.Font = pygame.font.Font(
            FONT_PATH + "Foldit-Medium.ttf", self.TITLE_FONT_SIZE
        )
        self.list_font: pygame.font.Font = pygame.font.Font(
            FONT_PATH + "barlow.ttf", self.LIST_FONT_SIZE
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

    def create_main_display_rect(self) -> pygame.Rect:
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

    # TODO: Add parameter for drawing backgrounds or not etc.
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the room items display on the given surface."""
        # Draw transparent background
        surface.blit(
            self.display_background, self.display_rect
        )  # draw background at display rect

        # border
        pygame.draw.rect(surface, (200, 200, 200), self.display_rect, 2)

        # title
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
                self.display_rect.y + ((i + 1) * (self.item_height // 2 + 10)) + 20,
                self.display_size.width - 30,
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
                item.name.upper(), True, self.TEXT_COLOR
            )

            surface.blit(
                item_text_surface,
                (
                    item_background_rect.x + 5,
                    item_background_rect.y + 2,
                ),
            )
