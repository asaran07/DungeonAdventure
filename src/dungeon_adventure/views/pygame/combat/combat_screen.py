import pygame
import logging
from typing import List, Dict, Tuple, Callable, Optional

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
HIGHLIGHT = (200, 200, 0)


class CombatScreen:
    def __init__(self, window_width: int, window_height: int):
        """
        Initialize the CombatScreen.

        :param window_width: Width of the game window
        :param window_height: Height of the game window
        """
        self._width = window_width
        self._height = window_height
        self._display = pygame.Surface((self._width - 50, self._height - 50))
        self.logger = logging.getLogger(__name__)
        self.panels: Dict[str, Dict] = {}
        self.available_actions: List[str] = []
        self.selected_action_index: int = 0
        self.selected_monster_index: int = -1
        self.selection_mode: str = "action"  # Can be "action" or "monster"
        self.combat_message: str = ""
        self.monsters: List = []

    @property
    def display(self) -> pygame.Surface:
        return self._display

    @display.setter
    def display(self, surface: pygame.Surface) -> None:
        self._display = surface

    def create_panel(
        self, name: str, size: Tuple[int, int], position: Tuple[int, int]
    ) -> None:
        """Create a new panel and add it to the panels dictionary."""
        panel = pygame.Surface(size)
        self.panels[name] = {"surface": panel, "position": position, "visible": False}

    def toggle_panel(self, name: str, visible: bool) -> None:
        """Toggle the visibility of a panel."""
        if name in self.panels:
            self.panels[name]["visible"] = visible

    def update_panel(
        self, name: str, update_func: Callable[[pygame.Surface], None]
    ) -> None:
        """Update a specific panel using the provided update function."""
        if name in self.panels and self.panels[name]["visible"]:
            panel = self.panels[name]["surface"]
            update_func(panel)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the combat display and all visible panels."""
        self._display.fill(BLACK)
        pygame.draw.rect(self._display, WHITE, self._display.get_rect(), 2)

        # Draw the title
        self._draw_title()

        # Draw all visible panels
        for panel_info in self.panels.values():
            if panel_info["visible"]:
                self._display.blit(panel_info["surface"], panel_info["position"])

        # Draw the combat display on the main screen
        display_rect = self._display.get_rect(center=screen.get_rect().center)
        screen.blit(self._display, display_rect)

    def _draw_title(self) -> None:
        """Draw the 'BATTLE' title on the combat screen."""
        title_surface = pygame.font.Font(None, 48).render("BATTLE", True, WHITE)
        title_rect = title_surface.get_rect(center=self._display.get_rect().center)
        self._display.blit(title_surface, title_rect)

    def draw_player_info(self, panel: pygame.Surface, player) -> None:
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

    def setup_combat(
        self, player, monsters: List, available_actions: List[str]
    ) -> None:
        """Set up the combat screen with player, monsters, and available actions."""
        self.logger.debug(
            f"Setting up combat for {player.name} using {len(monsters)} monsters"
        )
        self.monsters = monsters
        self.available_actions = available_actions
        self._create_combat_panels()
        self._initialize_combat_panels(player)

    def _create_combat_panels(self) -> None:
        """Create all necessary panels for the combat screen."""
        self.create_panel("player_info", (200, 150), (10, 10))
        self.create_panel("monster_info", (200, 200), (10, 170))
        self.create_panel("actions", (200, 100), (220, 10))
        self.create_panel("messages", (400, 100), (100, 100))

    def _initialize_combat_panels(self, player) -> None:
        """Initialize and make visible all combat panels."""
        for panel_name in ["player_info", "monster_info", "actions", "messages"]:
            self.toggle_panel(panel_name, True)

        self.update_panel(
            "player_info", lambda panel: self.draw_player_info(panel, player)
        )
        self.update_monster_info()
        self.update_action_panel()

    def update_monster_info(self) -> None:
        """Update the monster info panel."""

        def draw_monster_info(panel: pygame.Surface) -> None:
            panel.fill(GRAY)
            pygame.draw.rect(panel, WHITE, panel.get_rect(), 2)
            font = pygame.font.Font(None, 24)
            y_offset = 10
            for i, monster in enumerate(self.monsters):
                color = (
                    HIGHLIGHT
                    if i == self.selected_monster_index
                    and self.selection_mode == "monster"
                    else WHITE
                )
                text = f"{monster.name}: HP {monster.current_hp}/{monster.max_hp}"
                text_surface = font.render(text, True, color)
                panel.blit(text_surface, (10, y_offset))
                y_offset += 30

        self.update_panel("monster_info", draw_monster_info)

    def update_action_panel(self) -> None:
        """Update the action panel."""

        def draw_actions(panel: pygame.Surface) -> None:
            panel.fill(GRAY)
            pygame.draw.rect(panel, WHITE, panel.get_rect(), 2)
            font = pygame.font.Font(None, 24)
            for i, action in enumerate(self.available_actions):
                color = (
                    HIGHLIGHT
                    if i == self.selected_action_index
                    and self.selection_mode == "action"
                    else WHITE
                )
                text_surface = font.render(action, True, color)
                panel.blit(text_surface, (10, 10 + i * 30))

        self.update_panel("actions", draw_actions)

    def set_combat_message(self, message: str) -> None:
        """Set and display a combat message."""
        self.combat_message = message

        def draw_message(panel: pygame.Surface) -> None:
            panel.fill(GRAY)
            pygame.draw.rect(panel, WHITE, panel.get_rect(), 2)
            font = pygame.font.Font(None, 24)
            text_surface = font.render(self.combat_message, True, WHITE)
            panel.blit(text_surface, (10, 10))

        self.update_panel("messages", draw_message)

    def handle_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input events for the combat screen."""
        if event.type == pygame.KEYDOWN:
            self.logger.debug(f"Keydown event in {self.selection_mode} mode")
            if self.selection_mode == "action":
                return self._handle_action_input(event)
            elif self.selection_mode == "monster":
                return self._handle_monster_input(event)

        return None

    def _handle_action_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input when in action selection mode."""
        if event.key == pygame.K_UP:
            self.selected_action_index = (self.selected_action_index - 1) % len(
                self.available_actions
            )
        elif event.key == pygame.K_DOWN:
            self.selected_action_index = (self.selected_action_index + 1) % len(
                self.available_actions
            )
        elif event.key == pygame.K_RETURN:
            if self.available_actions[self.selected_action_index] == "Attack":
                self.selection_mode = "monster"
                self.selected_monster_index = 0
            else:
                return "action_selected"
        self._update_combat_ui()
        return None

    def _handle_monster_input(self, event: pygame.event.Event) -> Optional[str]:
        """Handle input when in monster selection mode."""
        if event.key == pygame.K_UP:
            self.selected_monster_index = (self.selected_monster_index - 1) % len(
                self.monsters
            )
        elif event.key == pygame.K_DOWN:
            self.selected_monster_index = (self.selected_monster_index + 1) % len(
                self.monsters
            )
        elif event.key == pygame.K_RETURN:
            self.selection_mode = "action"
            return "monster_selected"
        elif event.key == pygame.K_ESCAPE:
            self.selection_mode = "action"
            self.selected_monster_index = -1
        self._update_combat_ui()
        return None

    def _update_combat_ui(self) -> None:
        """Update the combat UI after input handling."""
        self.update_monster_info()
        self.update_action_panel()

    def get_selected_action(self) -> str:
        """Get the currently selected action."""
        self.logger.debug("Getting selected action")
        return self.available_actions[self.selected_action_index]

    def get_selected_monster_index(self) -> int:
        """Get the index of the currently selected monster."""
        self.logger.debug("Getting selected monster index")
        return self.selected_monster_index

    def reset_selection(self) -> None:
        """Reset the selection state."""
        self.logger.debug("Resetting selection")
        self.selection_mode = "action"
        self.selected_action_index = 0
        self.selected_monster_index = -1
        self._update_combat_ui()

    def end_combat(self) -> None:
        """Clean up the combat screen state."""
        self.logger.debug("Ending combat")
        self.panels.clear()
        self.available_actions.clear()
        self.selected_action_index = 0
        self.selected_monster_index = -1
        self.selection_mode = "action"
        self.combat_message = ""
        self.monsters.clear()
