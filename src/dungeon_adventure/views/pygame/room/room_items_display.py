import pygame
from typing import List

from pygame import FONT_CENTER

from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.models.items import Item


class RoomItemsDisplay:
    def __init__(self, screen_width: int, screen_height: int, scale_factor: int):
        self.scale_factor = scale_factor
        self.display_width = 150 * scale_factor
        self.display_rect = pygame.Rect(
            10 * scale_factor,  # distance from the left edge of the screen
            10 * scale_factor,  # distance from the right edge of the screen
            self.display_width,  # width of the display rectangle
            200,  # height of the display rectangle
            # screen_height - (100 * scale_factor)  # full screen height minus the margins, we could also just do custom
        )
        self.font = pygame.font.Font(None, 12 * scale_factor)
        self.list_font = pygame.font.Font(None, 8 * scale_factor)
        self.item_height = 30 * scale_factor
        self.items: List[Item] = []

        # Create a transparent surface for the background
        self.background = pygame.Surface((self.display_rect.width, self.display_rect.height), pygame.SRCALPHA)
        self.background.fill((54, 32, 48, 60))  # RGBA: 50, 50, 50 is dark gray, 128 is 50% opacity

    def update(self, room: Room):
        self.items = room.items

    def draw(self, surface: pygame.Surface):
        # Draw background
        # pygame.draw.rect(surface, (50, 50, 50), self.display_rect)
        # pygame.draw.rect(surface, (200, 200, 200), self.display_rect, 2)

        # Draw transparent background
        surface.blit(self.background, self.display_rect)

        # Draw border
        # pygame.draw.rect(surface, (200, 200, 200), self.display_rect, 2)

        # Draw title
        title_surface = self.font.render("Room Items", True, (255, 255, 255))
        surface.blit(
            title_surface,
            (
                self.display_rect.x + (10 * self.scale_factor),
                self.display_rect.y + (10 * self.scale_factor),
            ),
        )

        # Draw items
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(
                self.display_rect.x + (5 * self.scale_factor),
                self.display_rect.y + ((i + 1) * self.item_height),
                self.display_width - (40 * self.scale_factor),
                self.item_height - (20 * self.scale_factor),
            )
            # pygame.draw.rect(surface, (100, 100, 100), item_rect)

            # Create a transparent surface for each item background
            item_background = pygame.Surface((item_rect.width, item_rect.height), pygame.SRCALPHA)
            item_background.fill((100, 100, 100, 128))  # RGBA: 100, 100, 100 is medium gray, 128 is 50% opacity

            surface.blit(item_background, item_rect)

            text_surface = self.list_font.render(item.name, True, (255, 255, 255))
            surface.blit(
                text_surface,
                (
                    item_rect.x + (5 * self.scale_factor),
                    item_rect.y + (2.5 * self.scale_factor),
                ),
            )

    def get_item_at_position(self, pos: tuple) -> Item:
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(
                self.display_rect.x + (5 * self.scale_factor),
                self.display_rect.y + ((i + 1) * self.item_height),
                self.display_width - (10 * self.scale_factor),
                self.item_height - (5 * self.scale_factor),
            )
            if item_rect.collidepoint(pos):
                return item
        return None
