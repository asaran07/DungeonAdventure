import pygame

from dungeon_adventure.views.pygame.game.game_screen import GameScreen
from dungeon_adventure.views.pygame.game.game_world import GameWorld
from dungeon_adventure.views.pygame.game.py_game_view import PyGameView
from dungeon_adventure.views.pygame.services.debug_manager import DebugManager


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

    def run(self) -> None:
        """Main game loop."""
        running: bool = True
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

        return True

    def update(self):
        """Update game state, GUI, and debug info."""
        dt = self.game_screen.tick(60)
        self.game_world.update(dt)
        self.pygame_view.update(self.game_world.current_room, self.game_world.room_dict)
        self.debug_manager.update_fps(self.game_screen.get_fps())

    def draw(self) -> None:
        """Draw the game world, GUI, and debug info if enabled."""
        self.game_screen.clear()

        # Draw the game world
        self.game_world.draw(self.game_screen.get_game_surface())

        # Draw debug information if debug mode is enabled
        if self.debug_manager.debug_mode:
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
