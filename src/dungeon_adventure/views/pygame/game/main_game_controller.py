import pygame

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
        self.key_bind_manager = KeyBindManager()

    def initialize(self):
        pygame.init()
        self.game_screen.initialize()
        self.pygame_view.initialize()
        self.game_world.initialize()

    def run(self):
        """Main Game Loop"""
        self.initialize()
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.game_screen.flip()
        pygame.quit()

    def handle_events(self) -> bool:
        """
        Handle pygame events.

        :return: False if the game should quit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.key_bind_manager.is_inventory_key(event):
                    self.pygame_view.toggle_inventory()
                elif event.key == pygame.K_b:
                    self.debug_manager.toggle_debug_mode()
                elif event.key == pygame.K_t:  # 'T' for Take
                    self.game_world.handle_take_item()
                elif event.key == pygame.K_x:  # 'X' for Drop
                    self.game_world.handle_drop_item()
                elif event.key == pygame.K_g:
                    self.pygame_view.room_items_display.toggle_visibility()

            # Handle inventory events if inventory is visible
            if self.pygame_view.inventory_display.is_visible:
                self.pygame_view.handle_event(event, self.game_world.composite_player.inventory)

        return True

    def update(self):
        """Update game state, GUI, and debug info."""
        dt = self.game_screen.tick(60)
        self.game_world.update(dt)
        self.pygame_view.update(self.game_world.current_room, self.game_world.room_dict)
        self.debug_manager.update_fps(self.game_screen.clock)

    def draw(self) -> None:
        """Draw the game world, GUI, and debug info if enabled."""
        self.game_screen.draw_background()

        # Draw the game world
        self.game_world.draw(self.game_screen.get_game_surface())

        # Draw debug information if debug mode is enabled
        if self.debug_manager.debug_mode:
            self.game_world.composite_player.py_player.draw_debug_info(self.game_screen.get_game_surface())
            self.game_world.draw_debug(self.game_screen.get_game_surface())
            self.debug_manager.draw_debug_info(
                self.game_screen.get_game_surface(), self.game_world
            )

        # Scale the game surface to the screen
        self.game_screen.blit_scaled()

        # Draw GUI elements if not in debug mode
        if not self.debug_manager.debug_mode:
            self.pygame_view.draw(
                self.game_screen.get_screen(),
                self.game_world.composite_player.inventory,
            )
