import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIPanel


class CombatScreen:
    def __init__(
        self, window_width: int, window_height: int, ui_manager: pygame_gui.UIManager
    ):
        self.window_width = window_width
        self.window_height = window_height
        self.ui_manager = ui_manager

        # Create main combat panel
        self.combat_panel = UIPanel(
            relative_rect=pygame.Rect(
                (50, 50), (window_width - 100, window_height - 100)
            ),
            manager=self.ui_manager,
        )

        # Player info
        self.player_panel = UIPanel(
            relative_rect=pygame.Rect((10, 10), (300, 200)),
            manager=self.ui_manager,
            container=self.combat_panel,
        )
        self.player_health_label = UILabel(
            relative_rect=pygame.Rect((10, 10), (280, 30)),
            text="Player HP: 100/100",
            manager=self.ui_manager,
            container=self.player_panel,
        )

        # Enemy info
        self.enemy_panel = UIPanel(
            relative_rect=pygame.Rect((window_width - 420, 10), (300, 200)),
            manager=self.ui_manager,
            container=self.combat_panel,
        )
        self.enemy_health_label = UILabel(
            relative_rect=pygame.Rect((10, 10), (280, 30)),
            text="Enemy HP: 50/50",
            manager=self.ui_manager,
            container=self.enemy_panel,
        )

        # Combat info
        self.combat_info_panel = UIPanel(
            relative_rect=pygame.Rect((10, 220), (window_width - 220, 200)),
            manager=self.ui_manager,
            container=self.combat_panel,
        )
        self.combat_info_label = UILabel(
            relative_rect=pygame.Rect((10, 10), (window_width - 240, 180)),
            text="Combat information will be displayed here.",
            manager=self.ui_manager,
            container=self.combat_info_panel,
        )

        # Action buttons
        self.action_panel = UIPanel(
            relative_rect=pygame.Rect(
                (10, window_height - 250), (window_width - 220, 140)
            ),
            manager=self.ui_manager,
            container=self.combat_panel,
        )
        self.attack_button = UIButton(
            relative_rect=pygame.Rect((10, 10), (150, 50)),
            text="Attack",
            manager=self.ui_manager,
            container=self.action_panel,
        )
        self.use_item_button = UIButton(
            relative_rect=pygame.Rect((170, 10), (150, 50)),
            text="Use Item",
            manager=self.ui_manager,
            container=self.action_panel,
        )
        self.flee_button = UIButton(
            relative_rect=pygame.Rect((330, 10), (150, 50)),
            text="Flee",
            manager=self.ui_manager,
            container=self.action_panel,
        )

    def process_events(self, event: pygame.event.Event):
        # The UI manager now handles all the event processing
        pass

    def update(self, time_delta: float):
        # The UI manager now handles all the updating
        pass

    def draw(self, surface: pygame.Surface):
        # The UI manager now handles all the drawing
        pass

    def update_player_info(self, player_health: int, player_max_health: int):
        self.player_health_label.set_text(
            f"Player HP: {player_health}/{player_max_health}"
        )

    def update_enemy_info(self, enemy_health: int, enemy_max_health: int):
        self.enemy_health_label.set_text(f"Enemy HP: {enemy_health}/{enemy_max_health}")

    def display_combat_message(self, message: str):
        self.combat_info_label.set_text(message)

    def set_action_callback(self, action: str, callback):
        if action == "attack":
            self.attack_button.on_pressed = callback
        elif action == "use_item":
            self.use_item_button.on_pressed = callback
        elif action == "flee":
            self.flee_button.on_pressed = callback
