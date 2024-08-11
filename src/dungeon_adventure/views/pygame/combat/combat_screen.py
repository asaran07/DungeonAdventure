import pygame
import logging

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class CombatScreen:
    def __init__(self, window_width: int, window_height: int):
        self._width = window_width
        self._height = window_height
        self._display = pygame.Surface((self._width - 50, self._height - 50))
        self.logger = logging.getLogger(__name__)
        self.panels = {}

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, surface: pygame.Surface):
        self._display = surface

    def create_panel(self, name: str, size: tuple, position: tuple):
        """Create a new panel and add it to the panels dictionary."""
        panel = pygame.Surface(size)
        self.panels[name] = {"surface": panel, "position": position, "visible": False}

    def toggle_panel(self, name: str, visible: bool):
        """Toggle the visibility of a panel."""
        if name in self.panels:
            self.panels[name]["visible"] = visible

    def update_panel(self, name: str, update_func):
        """Update a specific panel using the provided update function."""
        if name in self.panels and self.panels[name]["visible"]:
            panel = self.panels[name]["surface"]
            update_func(panel)

    def draw(self, screen: pygame.Surface):
        """Draw the combat display and all visible panels."""
        self._display.fill(BLACK)
        pygame.draw.rect(self._display, WHITE, self._display.get_rect(), 2)

        # Draw the title
        title_surface = pygame.font.Font(None, 48).render("BATTLE", True, WHITE)
        title_rect = title_surface.get_rect(center=self._display.get_rect().center)
        self._display.blit(title_surface, title_rect)

        # Draw all visible panels
        for panel_info in self.panels.values():
            if panel_info["visible"]:
                self._display.blit(panel_info["surface"], panel_info["position"])

        # Draw the combat display on the main screen
        display_rect = self._display.get_rect(center=screen.get_rect().center)
        screen.blit(self._display, display_rect)

    def draw_player_info(self, panel: pygame.Surface, player):
        """Draw player info on the given panel."""
        panel.fill((50, 50, 50))  # Dark gray background
        pygame.draw.rect(panel, WHITE, panel.get_rect(), 2)

        font = pygame.font.Font(None, 24)
        y_offset = 10
        line_spacing = 30

        info_lines = [
            f"Name: {player.name}",
            f"HP: {player.hero.current_hp}/{player.hero.max_hp}",
            f"XP: {player.hero.xp}/{player.hero.xp_to_next_level}",
            f"Level: {player.hero.level}",
            f"Weapon: {player.hero.equipped_weapon.name if player.hero.equipped_weapon else 'None'}",
            f"Attack: {player.hero.base_min_damage}-{player.hero.base_max_damage}",
            f"Hit Chance: {player.hero.base_hit_chance}%",
        ]

        for line in info_lines:
            text_surface = font.render(line, True, WHITE)
            panel.blit(text_surface, (10, y_offset))
            y_offset += line_spacing


# Example usage in CombatManager:
# combat_screen.create_panel("player_info", (300, 200), (10, 10))
# combat_screen.toggle_panel("player_info", True)
# combat_screen.update_panel("player_info", lambda panel: combat_screen.draw_player_info(panel, player))
# combat_screen.draw(screen)
