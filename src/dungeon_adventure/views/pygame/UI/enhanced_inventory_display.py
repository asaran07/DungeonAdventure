import pygame
from typing import List, Optional, Tuple

from dungeon_adventure.models.items import Item, Weapon


class EnhancedInventoryDisplay:
    def __init__(self, screen_width: int, screen_height: int, scale_factor: int = 3):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale_factor = scale_factor
        self.hovered_button = None
        self.current_item_info = None
        self.hovered_popup_button = None

        # Colors
        self.colors = {
            "background": "#78514F",
            "stroke": "#5E3A38",
            "panel": "#D9D9D9",
            "button": "#EFEFEF",
            "text": "#000000",
            'button_hover': '#D0D0D0',
            'xp_bar': '#2CC757',
            'hp_bar': '#C72C2C'
        }

        # Fonts
        self.fonts = {
            "button": pygame.font.Font(None, 10 * self.scale_factor),
            "info": pygame.font.Font(None, 8 * self.scale_factor),
        }

        # Panels
        self.background_panel = self.scale_rect(45, 25, 390, 219)
        self.inventory_panel = self.scale_rect(70, 40, 339, 189)
        self.item_info_panel = self.scale_rect(289, 55, 100, 80)
        self.player_info_panel = self.scale_rect(289, 144, 100, 67)

        # Buttons
        self.item_buttons = self.create_item_buttons()

        # Text areas
        self.item_info_text = self.scale_rect(295, 61, 88, 68)
        self.player_info_text = self.scale_rect(295, 152, 40, 53)

        # Bars
        self.xp_bar = self.scale_rect(339, 151, 17, 54)
        self.hp_bar = self.scale_rect(364, 151, 17, 54)

        # Popup
        self.popup = None
        self.popup_buttons = None

    def scale_rect(self, x: int, y: int, w: int, h: int) -> pygame.Rect:
        return pygame.Rect(
            x * self.scale_factor,
            y * self.scale_factor,
            w * self.scale_factor,
            h * self.scale_factor,
        )

    def create_item_buttons(self) -> List[pygame.Rect]:
        buttons = []
        for col in range(2):
            for row in range(5):
                x = 93 + col * (80 + 18)
                y = 55 + row * 34
                buttons.append(self.scale_rect(x, y, 80, 22))
        return buttons

    def draw(self, surface: pygame.Surface, player):
        # Draw panels
        pygame.draw.rect(surface, self.colors["background"], self.background_panel)
        pygame.draw.rect(
            surface, self.colors["stroke"], self.background_panel, 3 * self.scale_factor
        )
        pygame.draw.rect(surface, self.colors["panel"], self.inventory_panel)
        pygame.draw.rect(
            surface, self.colors["text"], self.inventory_panel, 2 * self.scale_factor
        )

        # Draw item buttons
        self.draw_item_buttons(surface, player.inventory)

        # Draw bars
        self.draw_bars(surface, player)

        # Draw info panels
        pygame.draw.rect(surface, self.colors["button"], self.item_info_panel)
        pygame.draw.rect(
            surface, self.colors["text"], self.item_info_panel, self.scale_factor
        )
        pygame.draw.rect(surface, self.colors["button"], self.player_info_panel)
        pygame.draw.rect(
            surface, self.colors["text"], self.player_info_panel, self.scale_factor
        )

        # Draw item info
        if self.current_item_info:
            self.draw_item_info(surface)

        # Draw text
        self.draw_player_info(surface, player)

        # Draw popup if active
        if self.popup:
            self.draw_popup(surface)

    def draw_item_buttons(self, surface: pygame.Surface, inventory):
        inventory_items = inventory.get_all_items()
        for i, button in enumerate(self.item_buttons):
            if i < len(inventory_items):
                item, quantity = inventory_items[i]
                color = self.colors['button_hover'] if button == self.hovered_button else self.colors['button']
                pygame.draw.rect(surface, color, button)
                pygame.draw.rect(surface, self.colors['text'], button, self.scale_factor)
                text = self.fonts['button'].render(f"{item.name} ({quantity})", True, self.colors['text'])
                text_rect = text.get_rect(center=button.center)
                surface.blit(text, text_rect)

    def draw_bars(self, surface: pygame.Surface, player):
        self.draw_stat_bar(surface, "XP", self.xp_bar, player.hero.xp / player.hero.xp_to_next_level)
        self.draw_stat_bar(surface, "HP", self.hp_bar, player.hero.current_hp / player.hero.max_hp)

    def draw_stat_bar(self, surface: pygame.Surface, stat_type: str, bar_rect: pygame.Rect, fill_ratio: float):
        pygame.draw.rect(surface, self.colors[f'{stat_type.lower()}_bar'], bar_rect)
        fill_height = int(bar_rect.height * fill_ratio)
        empty_rect = bar_rect.copy()
        empty_rect.height -= fill_height
        pygame.draw.rect(surface, self.colors['background'], empty_rect)
        pygame.draw.rect(surface, self.colors['text'], bar_rect, self.scale_factor)

    def draw_player_info(self, surface: pygame.Surface, player):
        info = f"HP: {player.hero.current_hp}/{player.hero.max_hp}\n"
        info += f"XP: {player.hero.xp}/{player.hero.xp_to_next_level}\n"
        info += f"Level: {player.hero.level}\n"
        info += f"Weight: {player.inventory.get_total_weight():.1f}/{player.inventory.weight_limit:.1f}"

        self.draw_text(surface, info, self.player_info_text)

    def draw_text(self, surface: pygame.Surface, text: str, rect: pygame.Rect):
        words = text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            if self.fonts["info"].size(test_line)[0] <= rect.width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))

        y = rect.top
        for line in lines:
            text_surface = self.fonts["info"].render(line, True, self.colors["text"])
            surface.blit(text_surface, (rect.left, y))
            y += self.fonts["info"].get_linesize()

    def handle_event(
        self, event: pygame.event.Event, player
    ) -> Optional[Tuple[str, str]]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.popup:
                return self.handle_popup_click(event.pos)
            else:
                return self.handle_button_click(event.pos, player.inventory)
        elif event.type == pygame.MOUSEMOTION:
            self.handle_hover(event.pos, player.inventory)

        return None

    def handle_button_click(
        self, pos: Tuple[int, int], inventory
    ) -> Optional[Tuple[str, str]]:
        inventory_items = inventory.get_all_items()
        for i, button in enumerate(self.item_buttons):
            if i < len(inventory_items) and button.collidepoint(pos):
                self.show_popup(inventory_items[i][0].id, inventory)
                return None
        return None

    def handle_popup_click(self, pos: Tuple[int, int]) -> Optional[Tuple[str, str]]:
        for action, button in self.popup_buttons.items():
            if button.collidepoint(pos):
                item_id = self.popup['item_id']
                self.close_popup()
                return (action, item_id)
        self.close_popup()
        return None

    def handle_hover(self, pos: Tuple[int, int], inventory):
        inventory_items = inventory.get_all_items()
        self.hovered_button = None
        self.hovered_popup_button = None

        for i, button in enumerate(self.item_buttons):
            if i < len(inventory_items) and button.collidepoint(pos):
                self.hovered_button = button
                if self.current_item_info != inventory_items[i][0]:
                    self.current_item_info = self.get_item_info(inventory_items[i][0])
                return

        if self.popup:
            for action, button in self.popup_buttons.items():
                if button.collidepoint(pos):
                    self.hovered_popup_button = action
                    return

    def get_item_info(self, item: Item) -> str:
        info = f"{item.name}\n\n"
        info += f"Type: {item.item_type.name}\n"
        info += f"Weight: {item.weight}\n\n"
        if isinstance(item, Weapon):
            info += f"Damage: {item.min_damage}-{item.max_damage}\n\n"
        info += f"{item.description}"
        return info

    def draw_item_info(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.colors['button'], self.item_info_panel)
        pygame.draw.rect(surface, self.colors['text'], self.item_info_panel, self.scale_factor)
        self.draw_text(surface, self.current_item_info, self.item_info_text)

    def show_popup(self, item_id: str, inventory):
        self.popup = {
            'panel': self.scale_rect(178, 98, 133, 75),
            'inner_panel': self.scale_rect(187, 106, 115, 57),
            'item_id': item_id
        }
        self.popup_buttons = {
            'use': self.scale_rect(204, 115, 83, 17),
            'drop': self.scale_rect(204, 136, 83, 17)
        }

        item = inventory.get_item_by_id(item_id)
        if isinstance(item, Weapon):
            self.popup_buttons['equip'] = self.scale_rect(204, 157, 83, 17)
            self.popup['panel'].height += 21 * self.scale_factor
            self.popup['inner_panel'].height += 21 * self.scale_factor

    def close_popup(self):
        self.popup = None
        self.popup_buttons = None

    def draw_popup(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.colors['background'], self.popup['panel'])
        pygame.draw.rect(surface, self.colors['stroke'], self.popup['panel'], 3 * self.scale_factor)
        pygame.draw.rect(surface, self.colors['button'], self.popup['inner_panel'])
        pygame.draw.rect(surface, self.colors['text'], self.popup['inner_panel'], self.scale_factor)

        for action, button in self.popup_buttons.items():
            color = self.colors['button_hover'] if self.hovered_popup_button == action else self.colors['button']
            pygame.draw.rect(surface, color, button)
            pygame.draw.rect(surface, self.colors['text'], button, self.scale_factor)
            text = self.fonts['button'].render(action.capitalize(), True, self.colors['text'])
            text_rect = text.get_rect(center=button.center)
            surface.blit(text, text_rect)

    def show_item_info(self, item: Item):
        info = f"{item.name}\n\n"
        info += f"Type: {item.item_type.name}\n"
        info += f"Weight: {item.weight}\n\n"
        info += f"{item.description}"
        self.draw_text(pygame.display.get_surface(), info, self.item_info_text)

    def clear_item_info(self):
        pygame.draw.rect(pygame.display.get_surface(), self.colors['button'], self.item_info_panel)
        pygame.draw.rect(pygame.display.get_surface(), self.colors['button'], self.item_info_panel)
        pygame.draw.rect(pygame.display.get_surface(), self.colors['text'], self.item_info_panel, self.scale_factor)
