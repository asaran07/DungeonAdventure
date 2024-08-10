import pygame
from typing import Dict, List, Tuple, Optional

from dungeon_adventure.config import FONT_PATH
from dungeon_adventure.enums.item_types import PotionType
from dungeon_adventure.models.inventory.inventory import Inventory
from dungeon_adventure.models.items.item import Item
from dungeon_adventure.models.items.weapon import Weapon
from dungeon_adventure.models.items.potion import Potion


class InventoryDisplay:
    def __init__(self, screen_width: int, screen_height: int, scale_factor: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale_factor = scale_factor
        self.width = int(screen_width + 100)
        self.height = int(screen_height)
        self.x = ((screen_width * 2) - self.width)
        self.y = ((screen_height * 3) - self.height)
        self.columns = 3
        self.padding = 1
        self.item_size = (
            (self.width // self.columns - self.padding * 2),
            50 * scale_factor,
        )
        self.title_font = pygame.font.Font(
            FONT_PATH + "Foldit-Medium.ttf", 24
        )
        self.item_font = pygame.font.Font(FONT_PATH + "barlow.ttf", 16 * scale_factor)
        self.selected_item: Optional[Item] = None
        self.visible = False

    def toggle_visibility(self):
        self.visible = not self.visible

    def draw(self, surface: pygame.Surface, inventory: Inventory):
        if not self.visible:
            return

        # Draw main inventory window
        pygame.draw.rect(
            surface, (50, 50, 50), (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            surface, (200, 200, 200), (self.x, self.y, self.width, self.height), 2
        )

        # Draw title
        title_surface = self.title_font.render("Inventory", True, (255, 255, 255))
        surface.blit(title_surface, (self.x + 10, self.y + 10))

        # Draw items
        items = inventory.get_all_items()
        for i, (item, quantity) in enumerate(items):
            col = i % self.columns
            row = i // self.columns
            item_x = self.x + col * (self.width // self.columns) + self.padding
            item_y = (
                self.y
                + row * (self.item_size[1] + self.padding)
                + self.padding
                + 50 * self.scale_factor
            )

            # Draw item background
            item_rect = pygame.Rect(item_x, item_y, *self.item_size)
            pygame.draw.rect(surface, (100, 100, 100), item_rect)

            # Highlight selected item
            if item == self.selected_item:
                pygame.draw.rect(surface, (255, 255, 0), item_rect, 2)

            # Draw item name and quantity
            text = f"{item.name} x{quantity}"
            text_surface = self.item_font.render(text, True, (255, 255, 255))
            surface.blit(text_surface, (item_x + 5, item_y + 5))

        # Draw item details if an item is selected
        if self.selected_item:
            self.draw_item_details(surface)

    def draw_item_details(self, surface: pygame.Surface):
        detail_width = 200 * self.scale_factor
        detail_height = 150 * self.scale_factor
        detail_x = self.x + self.width
        detail_y = self.y

        # Draw detail window
        pygame.draw.rect(
            surface, (70, 70, 70), (detail_x, detail_y, detail_width, detail_height)
        )
        pygame.draw.rect(
            surface,
            (200, 200, 200),
            (detail_x, detail_y, detail_width, detail_height),
            2,
        )

        # Draw item details
        lines = [
            f"Name: {self.selected_item.name}",
            f"Weight: {self.selected_item.weight}",
            f"Description: {self.selected_item.description}",
        ]

        if isinstance(self.selected_item, Weapon):
            lines.extend(
                [
                    f"Damage: {self.selected_item.min_damage}-{self.selected_item.max_damage}",
                    f"Durability: {self.selected_item.durability}",
                ]
            )
        elif isinstance(self.selected_item, Potion):
            lines.append(f"Healing: {self.selected_item.heal_amount}")

        for i, line in enumerate(lines):
            text_surface = self.item_font.render(line, True, (255, 255, 255))
            surface.blit(
                text_surface, (detail_x + 5, detail_y + 5 + i * 25 * self.scale_factor)
            )

    def handle_event(self, event: pygame.event.Event, inventory: Inventory) -> bool:
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            items = inventory.get_all_items()
            for i, (item, _) in enumerate(items):
                col = i % self.columns
                row = i // self.columns
                item_x = self.x + col * (self.width // self.columns) + self.padding
                item_y = (
                    self.y
                    + row * (self.item_size[1] + self.padding)
                    + self.padding
                    + 50 * self.scale_factor
                )
                item_rect = pygame.Rect(item_x, item_y, *self.item_size)
                if item_rect.collidepoint(mouse_pos):
                    self.selected_item = item
                    return True
        return False

    def is_point_inside(self, point: Tuple[int, int]) -> bool:
        return (
            self.x <= point[0] <= self.x + self.width
            and self.y <= point[1] <= self.y + self.height
        )
