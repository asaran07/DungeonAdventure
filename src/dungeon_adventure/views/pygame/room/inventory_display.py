import pygame

from dungeon_adventure.config import FONT_PATH
from src.dungeon_adventure.models.inventory.inventory import Inventory


class InventoryDisplay:
    def __init__(self, screen_width: int, screen_height: int, scale_factor: int):
        self.scale_factor = scale_factor
        self.inventory_height = 60 * scale_factor
        self.inventory_rect = pygame.Rect(
            10 * scale_factor,
            screen_height - self.inventory_height - (10 * scale_factor),
            screen_width - (20 * scale_factor),
            self.inventory_height,
        )
        self.inventory_font = pygame.font.Font(
            FONT_PATH + "courier_prime.ttf",
            15 * scale_factor,
        )

    def draw(self, surface: pygame.Surface, inventory: Inventory):
        # Draw inventory background
        pygame.draw.rect(surface, (0, 0, 0), self.inventory_rect)
        pygame.draw.rect(surface, (200, 200, 200), self.inventory_rect, 2)

        # Get inventory string
        inventory_str = str(inventory)

        # Render inventory text
        lines = inventory_str.split("\n")
        for i, line in enumerate(lines):
            text_surface = self.inventory_font.render(line, True, (255, 255, 255))
            surface.blit(
                text_surface,
                (
                    self.inventory_rect.x + (5 * self.scale_factor),
                    self.inventory_rect.y
                    + (5 * self.scale_factor)
                    + i * (20 * self.scale_factor),
                ),
            )

    def is_point_inside(self, point: tuple) -> bool:
        return self.inventory_rect.collidepoint(point)

    # We can add more methods here for interactivity like
    # def handle_click(self, point: tuple, inventory: Inventory):
    #     # Handle clicking on inventory items
    #     pass
