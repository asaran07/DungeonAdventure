from typing import Optional, List, Tuple

import pygame

from dungeon_adventure.models.inventory.inventory import Inventory
from dungeon_adventure.models.items.item import Item
from dungeon_adventure.models.items.weapon import Weapon
from dungeon_adventure.models.items.potion import Potion


class InventoryDisplay:
    def __init__(self, screen_width: int, screen_height: int, scale_factor: int):
        self.screen_width = screen_width * scale_factor
        self.screen_height = screen_height * scale_factor
        self.scale_factor = scale_factor
        self.is_visible = False
        self.inventory: Optional[Inventory] = None
        self.hovered_index = -1
        self.font = pygame.font.Font(None, 24)

        # Initialize display properties
        self.display_width = int(self.screen_width * 0.6)
        self.display_height = int(self.screen_height * 0.6)
        self.display_x = (self.screen_width - self.display_width) // 2
        self.display_y = (self.screen_height - self.display_height) // 2
        self.columns = 2
        self.rows = 5
        self.item_width = (self.display_width // self.columns) - 60
        self.item_height = (self.display_height // self.rows) - 60

        self.item_details_popup = ItemDetailsPopup(
            self.screen_width, self.screen_height, self.scale_factor
        )

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered_index = self.get_item_at_position(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                clicked_index = self.get_item_at_position(event.pos)
                if clicked_index is not None:
                    self.show_item_details(
                        self.inventory.get_all_items()[clicked_index][0]
                    )

    def get_item_at_position(self, pos: tuple[int, int]) -> Optional[int]:
        x, y = pos
        if (
            self.display_x <= x <= self.display_x + self.display_width
            and self.display_y <= y <= self.display_y + self.display_height
        ):
            col = (x - self.display_x) // (self.item_width + 60)
            row = (y - self.display_y) // (self.item_height + 60)
            index = row * self.columns + col
            if 0 <= index < len(self.inventory.get_all_items()):
                return index
        return None

    def show_item_details(self, item: Item):
        self.item_details_popup.show(item)

    def draw(self, surface: pygame.Surface, inventory: Inventory):
        self.inventory = inventory

        # Draw background
        pygame.draw.rect(
            surface,
            (50, 50, 50),
            (self.display_x, self.display_y, self.display_width, self.display_height),
        )
        pygame.draw.rect(
            surface,
            (200, 200, 200),
            (self.display_x, self.display_y, self.display_width, self.display_height),
            2,
        )

        # Draw items
        items: List[Tuple[Item, int]] = self.inventory.get_all_items()
        for i, (item, quantity) in enumerate(items):
            row = i // self.columns
            col = i % self.columns
            item_x = self.display_x + col * (self.item_width + 60) + 30
            item_y = self.display_y + row * (self.item_height + 60) + 30

            # Draw item background
            if i == self.hovered_index:
                bg_color = (100, 100, 100)  # Hovered item color
            else:
                bg_color = (75, 75, 75)  # Default item color

            pygame.draw.rect(
                surface, bg_color, (item_x, item_y, self.item_width, self.item_height)
            )

            # Draw item name and quantity
            item_text = f"{item.name} (x{quantity})"
            item_name = self.font.render(item_text, True, (255, 255, 255))
            surface.blit(item_name, (item_x + 5, item_y + 5))

        # Draw total weight
        weight_text = f"Total Weight: {self.inventory.get_total_weight():.1f}/{self.inventory.weight_limit:.1f}"
        weight_surface = self.font.render(weight_text, True, (255, 255, 255))
        surface.blit(
            weight_surface,
            (self.display_x + 5, self.display_y + self.display_height - 30),
        )

        # Draw item details popup
        self.item_details_popup.draw(surface)


class ItemDetailsPopup:
    def __init__(self, screen_width: int, screen_height: int, scale_factor: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale_factor = scale_factor
        self.is_visible = False
        self.item: Optional[Item] = None
        self.font = pygame.font.Font(None, 24)

        # Initialize popup properties
        self.popup_width = int(self.screen_width * 0.3)
        self.popup_height = int(self.screen_height * 0.4)  # Increased height
        self.popup_x = (self.screen_width - self.popup_width) // 2
        self.popup_y = (self.screen_height - self.popup_height) // 2

    def show(self, item: Item):
        self.is_visible = True
        self.item = item

    def hide(self):
        self.is_visible = False
        self.item = None

    def draw(self, surface: pygame.Surface):
        if not self.is_visible or self.item is None:
            return

        # Draw background
        pygame.draw.rect(
            surface,
            (75, 75, 75),
            (self.popup_x, self.popup_y, self.popup_width, self.popup_height),
        )
        pygame.draw.rect(
            surface,
            (200, 200, 200),
            (self.popup_x, self.popup_y, self.popup_width, self.popup_height),
            2,
        )

        # Draw item details
        y_offset = 10
        line_height = 30

        # Item name
        self._draw_text(surface, f"Name: {self.item.name}", y_offset)
        y_offset += line_height

        # Item type
        self._draw_text(surface, f"Type: {self.item.__class__.__name__}", y_offset)
        y_offset += line_height

        # Item weight
        self._draw_text(surface, f"Weight: {self.item.weight}", y_offset)
        y_offset += line_height

        # Item-specific details
        if isinstance(self.item, Weapon):
            self._draw_text(
                surface,
                f"Damage: {self.item.min_damage}-{self.item.max_damage}",
                y_offset,
            )
            y_offset += line_height
        elif isinstance(self.item, Potion):
            if hasattr(self.item, "heal_amount"):
                self._draw_text(surface, f"Heals: {self.item.heal_amount} HP", y_offset)
                y_offset += line_height

        # Item description (multi-line)
        description_lines = self._wrap_text(
            self.item.description, self.popup_width - 20
        )
        for line in description_lines:
            self._draw_text(surface, line, y_offset)
            y_offset += line_height

    def _draw_text(self, surface: pygame.Surface, text: str, y_offset: int):
        text_surface = self.font.render(text, True, (255, 255, 255))
        surface.blit(text_surface, (self.popup_x + 10, self.popup_y + y_offset))

    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            if self.font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))
        return lines
