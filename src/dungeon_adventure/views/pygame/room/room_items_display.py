import pygame
from typing import List

from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.models.items import Item


class RoomItemsDisplay:
    def __init__(self, screen_width: int, screen_height: int, scale_factor: int):
        self.scale_factor = scale_factor
        self.display_width = 150 * scale_factor
        self.display_rect = pygame.Rect(
            10 * scale_factor,
            10 * scale_factor,
            self.display_width,
            screen_height - (100 * scale_factor)
        )
        self.font = pygame.font.Font(None, 18 * scale_factor)
        self.item_height = 30 * scale_factor
        self.items: List[Item] = []

    def update(self, room: Room):
        self.items = room.items

    def draw(self, surface: pygame.Surface):
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), self.display_rect)
        pygame.draw.rect(surface, (200, 200, 200), self.display_rect, 2)

        # Draw title
        title_surface = self.font.render("Room Items", True, (255, 255, 255))
        surface.blit(title_surface, (self.display_rect.x + (10 * self.scale_factor), self.display_rect.y + (10 * self.scale_factor)))

        # Draw items
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(
                self.display_rect.x + (5 * self.scale_factor),
                self.display_rect.y + ((i + 1) * self.item_height),
                self.display_width - (10 * self.scale_factor),
                self.item_height - (5 * self.scale_factor)
            )
            pygame.draw.rect(surface, (100, 100, 100), item_rect)
            text_surface = self.font.render(item.name, True, (255, 255, 255))
            surface.blit(text_surface, (item_rect.x + (5 * self.scale_factor), item_rect.y + (5 * self.scale_factor)))

    def get_item_at_position(self, pos: tuple) -> Item:
        for i, item in enumerate(self.items):
            item_rect = pygame.Rect(
                self.display_rect.x + (5 * self.scale_factor),
                self.display_rect.y + ((i + 1) * self.item_height),
                self.display_width - (10 * self.scale_factor),
                self.item_height - (5 * self.scale_factor)
            )
            if item_rect.collidepoint(pos):
                return item
        return None