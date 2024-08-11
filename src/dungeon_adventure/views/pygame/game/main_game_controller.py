import logging
from typing import Dict, Callable

import pygame

from dungeon_adventure.enums.game_state import GameState
from dungeon_adventure.views.pygame.game.combat_manager import CombatManager
from dungeon_adventure.views.pygame.game.game_screen import GameScreen
from dungeon_adventure.views.pygame.game.game_world import GameWorld
from dungeon_adventure.views.pygame.game.py_game_view import PyGameView
from dungeon_adventure.views.pygame.services.debug_manager import DebugManager
from dungeon_adventure.views.pygame.services.keybind_manager import KeyBindManager


class MainGameController:
    def __init__(
        self,
        game_world: GameWorld,
        game_screen: GameScreen,
        pygame_view: PyGameView,
        debug_manager: DebugManager,
    ):
        """
        Initialize the GameController with necessary components.

        :param game_world: The game world containing game logic and state
        :param game_screen: The game screen for rendering
        :param pygame_view: The GUI manager for handling UI elements
        :param debug_manager: The debug manager for debug-related functionality
        """
        self.game_world: GameWorld = game_world
        self.game_screen: GameScreen = game_screen
        self.pygame_view: PyGameView = pygame_view
        self.debug_manager: DebugManager = debug_manager
        self.key_bind_manager: KeyBindManager = KeyBindManager()
        self.combat_manager: CombatManager = CombatManager(self.game_world)
        self.game_world.on_combat_initiated = self.initiate_combat
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

        self.key_actions: Dict[int, Callable] = {
            pygame.K_i: lambda: self.pygame_view.toggle_visibility("inventory"),
            pygame.K_b: self.debug_manager.toggle_debug_mode,
            pygame.K_t: self.game_world.handle_take_item,
            pygame.K_x: self.game_world.handle_drop_item,
            pygame.K_g: lambda: self.pygame_view.toggle_visibility("room_items"),
            pygame.K_m: lambda: self.pygame_view.toggle_visibility("minimap"),
            pygame.K_c: lambda: self.pygame_view.toggle_visibility("combat_screen"),
            pygame.K_h: lambda: self.pygame_view.toggle_visibility("controls"),
        }

    def initiate_combat(self) -> None:
        """Initiate combat when triggered by the game world."""
        self.logger.debug("Initiating combat", stacklevel=2)
        self.combat_manager.initiate_combat()

    def initialize(self) -> None:
        """Initialize all game components."""
        pygame.init()
        self.logger.debug("Initializing game components", stacklevel=2)
        self.game_screen.initialize()
        self.pygame_view.initialize()
        self.game_world.initialize()

    def run(self) -> None:
        """Main Game Loop"""
        self.logger.info("Starting game loop")
        self.initialize()
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.game_screen.flip()
        self.logger.info("Game loop ended")
        pygame.quit()

    def handle_events(self) -> bool:
        """
        Handle pygame events.

        :return: False if the game should quit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.info("Quit event received")
                return False
            self._handle_keydown_event(event)
            self._handle_combat_events(event)
        return True

    def _handle_keydown_event(self, event: pygame.event.Event) -> None:
        """Handle keydown events."""
        if (
            event.type == pygame.KEYDOWN
            and self.game_world.game_model.game_state != GameState.IN_COMBAT
        ):
            action = self.key_actions.get(event.key)
            if action:
                action()

    def _handle_combat_events(self, event: pygame.event.Event) -> None:
        """Handle combat and inventory-specific events."""
        if self.game_world.game_model.game_state == GameState.IN_COMBAT:
            self.combat_manager.handle_event(event)

    def _handle_inventory_events(self, event: pygame.event.Event) -> None:
        if self.pygame_view.inventory_visible:
            self.pygame_view.handle_event(event)

    def update(self) -> None:
        """Update game state, GUI, and debug info."""
        dt = self.game_screen.tick(60)
        self.game_world.update(dt)
        self.pygame_view.update(self.game_world.current_room, self.game_world.room_dict)
        self.debug_manager.update_fps(self.game_screen.clock)

        if self.game_world.game_model.game_state == GameState.IN_COMBAT:
            self.combat_manager.update()

    def draw(self) -> None:
        """Draw the game world, GUI, and debug info if enabled."""
        self.game_screen.draw_background()
        self._draw_game_world()
        self._draw_debug_info()
        self.game_screen.blit_scaled()
        # The GUI elements made with Pygame components are draw directly onto the screen, instead of the game_surface.
        self._draw_gui()

    def _draw_game_world(self) -> None:
        """Draw the game world and combat screen if in combat."""
        self.game_world.draw(self.game_screen.get_game_surface())
        if self.game_world.game_model.game_state == GameState.IN_COMBAT:
            self.combat_manager.draw()

    def _draw_debug_info(self) -> None:
        """Draw debug information if debug mode is enabled."""
        if self.debug_manager.debug_mode:
            self.game_world.composite_player.py_player.draw_debug_info(
                self.game_screen.get_game_surface()
            )
            self.game_world.draw_debug(self.game_screen.get_game_surface())
            self.debug_manager.draw_debug_info(
                self.game_screen.get_game_surface(), self.game_world
            )

    def _draw_gui(self) -> None:
        """Draw GUI elements if not in debug mode."""
        if not self.debug_manager.debug_mode:
            self.pygame_view.draw(
                self.game_screen.get_screen(),
                self.game_world.composite_player.inventory,
            )
