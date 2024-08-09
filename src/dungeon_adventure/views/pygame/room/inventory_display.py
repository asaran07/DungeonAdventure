from collections import namedtuple
from typing import Tuple

import pygame

from dungeon_adventure.config import FONT_PATH
from dungeon_adventure.models.inventory.inventory import Inventory


class InventoryDisplay:
    # Constants for sizing and positioning
    DISPLAY_WIDTH_FACTOR: float = 160
    DISPLAY_HEIGHT_FACTOR: float = 60
    X_POS_FACTOR: float = 0.33  # 33% from left edge
    Y_POS_FACTOR: float = 0.70  # 85% from top edge
    TITLE_FONT_SIZE: int = 12
    ITEM_FONT_SIZE: int = 8
    ITEM_HEIGHT_FACTOR: float = 0.2
    ITEM_HORIZONTAL_MARGIN: int = 5
    ITEM_VERTICAL_MARGIN: int = 3

    # Colors
    BACKGROUND_COLOR: Tuple[int, int, int, int] = (0, 0, 0, 200)  # RGBA
    BORDER_COLOR: Tuple[int, int, int] = (200, 200, 200)  # Light gray
    TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)  # White
    ITEM_BACKGROUND_COLOR: Tuple[int, int, int, int] = (100, 100, 100, 128)  # RGBA

    Position = namedtuple("Position", ["x", "y"])
    Size = namedtuple("Size", ["width", "height"])

    def __init__(self, screen_width: int, screen_height: int, scale_factor: int):
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.scale_factor: int = scale_factor

        self.display_size = self.calc_display_size()
        self.display_pos = self.calc_display_pos()
        self.display_rect = self.create_main_display_rect()

        self.title_font: pygame.font.Font = pygame.font.Font(
            FONT_PATH + "Foldit-Medium.ttf", self.TITLE_FONT_SIZE * scale_factor
        )
        self.item_font: pygame.font.Font = pygame.font.Font(
            FONT_PATH + "barlow.ttf", self.ITEM_FONT_SIZE * scale_factor
        )

        self.item_height: int = int(self.ITEM_HEIGHT_FACTOR * self.display_rect.height)

        # Create a transparent surface for the background
        self.display_background: pygame.Surface = pygame.Surface(
            (self.display_rect.width, self.display_rect.height), pygame.SRCALPHA
        )
        self.display_background.fill(self.BACKGROUND_COLOR)

    def calc_display_size(self) -> Size:
        display_width: int = int(self.DISPLAY_WIDTH_FACTOR * self.scale_factor)
        display_height: int = int(self.DISPLAY_HEIGHT_FACTOR * self.scale_factor)
        return self.Size(display_width, display_height)

    def calc_display_pos(self) -> Position:
        display_pos_x: int = int(self.screen_width * self.X_POS_FACTOR)
        display_pos_y: int = int(self.screen_height * self.Y_POS_FACTOR)
        return self.Position(display_pos_x, display_pos_y)

    def create_main_display_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.display_pos.x,
            self.display_pos.y,
            self.display_size.width,
            self.display_size.height,
        )

    def draw(self, surface: pygame.Surface, inventory: Inventory):
        # Draw background
        surface.blit(self.display_background, self.display_rect)

        # Draw border
        pygame.draw.rect(surface, self.BORDER_COLOR, self.display_rect, 2)

        # Draw title
        title_surface: pygame.Surface = self.title_font.render(
            "Inventory", True, self.TEXT_COLOR
        )
        title_rect = title_surface.get_rect(
            midtop=(self.display_rect.centerx, self.display_rect.top + 5)
        )
        surface.blit(title_surface, title_rect)

        # Draw inventory items
        items = inventory.get_all_items()
        start_y = title_rect.bottom + 10
        for i, (item, quantity) in enumerate(items):
            item_rect = pygame.Rect(
                self.display_rect.x + self.ITEM_HORIZONTAL_MARGIN * self.scale_factor,
                start_y
                + i
                * (self.item_height + self.ITEM_VERTICAL_MARGIN * self.scale_factor),
                self.display_rect.width
                - 2 * self.ITEM_HORIZONTAL_MARGIN * self.scale_factor,
                self.item_height,
            )

            # Draw item background
            pygame.draw.rect(surface, self.ITEM_BACKGROUND_COLOR, item_rect)

            # Draw item text
            item_text = f"{item.name} x{quantity}"
            item_surface = self.item_font.render(item_text, True, self.TEXT_COLOR)
            item_text_rect = item_surface.get_rect(
                midleft=(item_rect.left + 5, item_rect.centery)
            )
            surface.blit(item_surface, item_text_rect)

        # Draw total weight
        weight_text = f"Total Weight: {inventory.get_total_weight():.1f}/{inventory.weight_limit:.1f}"
        weight_surface = self.item_font.render(weight_text, True, self.TEXT_COLOR)
        weight_rect = weight_surface.get_rect(
            midbottom=(self.display_rect.centerx, self.display_rect.bottom - 5)
        )
        surface.blit(weight_surface, weight_rect)

    def is_point_inside(self, point: Tuple[int, int]) -> bool:
        return self.display_rect.collidepoint(point)
