import logging
from typing import Callable, Dict

import pygame

from dungeon_adventure.config import RESOURCES_DIR
from dungeon_adventure.enums.game_state import GameState
from dungeon_adventure.enums.room_types import RoomType
from dungeon_adventure.game_model import GameModel
from dungeon_adventure.models.player.player import Player
from dungeon_adventure.services.dungeon_generator import DungeonGenerator
from dungeon_adventure.views.pygame.combat.combat_screen import CombatScreen
from dungeon_adventure.views.pygame.game.combat_manager import CombatManager
from dungeon_adventure.views.pygame.game.game_screen import GameScreen
from dungeon_adventure.views.pygame.game.game_world import GameWorld
from dungeon_adventure.views.pygame.game.py_game_view import PyGameView
from dungeon_adventure.views.pygame.services.debug_manager import DebugManager
from dungeon_adventure.views.pygame.services.keybind_manager import KeyBindManager
from dungeon_adventure.views.pygame.sprites.composite_player import CompositePlayer
from dungeon_adventure.views.pygame.sprites.py_player import PyPlayer
from serialization.game_snapshot import save_game, GameSnapshotPygame, load_game


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

        :param game_world: The game world contains game logic and state
        :param game_screen: The game screen for rendering
        :param pygame_view: The GUI manager for handling UI elements
        :param debug_manager: The debug manager for debug-related functionality
        """
        self.game_world: GameWorld = game_world
        self.game_screen: GameScreen = game_screen
        self.pygame_view: PyGameView = pygame_view
        self.debug_manager: DebugManager = debug_manager
        self.key_bind_manager: KeyBindManager = KeyBindManager()
        self.debug_mode = False

        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        pygame.init()
        pygame.mixer.init()
        self.load_and_play_music()

        # Set up the display
        self.screen = pygame.display.set_mode(
            (
                self.game_screen.width * self.game_screen.scale_factor,
                self.game_screen.height * self.game_screen.scale_factor,
            )
        )

        # Initialize CombatScreen
        self.combat_screen = CombatScreen(
            self.game_screen.width * self.game_screen.scale_factor,
            self.game_screen.height * self.game_screen.scale_factor,
        )

        # Initialize CombatManager with CombatScreen
        self.combat_manager: CombatManager = CombatManager(self.game_world)
        self.combat_manager.set_combat_screen(self.combat_screen)

        self.game_world.on_combat_initiated = self.initiate_combat
        self.game_world.on_items_in_room = self.show_room_items
        self.game_world.pit_encounter = self.handle_pit_encounter
        self.game_world.on_room_enter = self.handle_room_enter
        self.game_world.on_win_condition = self.handle_win_condition
        self.lose_condition = False
        self.game_world.on_combat_end = self.handle_combat_end

        self.key_actions: Dict[int, Callable] = {
            pygame.K_i: lambda: self.pygame_view.toggle_visibility("inventory"),
            pygame.K_b: self.debug_manager.toggle_debug_mode,
            pygame.K_t: self.game_world.handle_take_item,
            pygame.K_x: self.game_world.handle_drop_item,
            pygame.K_g: lambda: self.pygame_view.toggle_visibility("room_items"),
            pygame.K_m: lambda: self.pygame_view.toggle_visibility("minimap"),
            pygame.K_c: lambda: self.pygame_view.toggle_visibility("combat_screen"),
            pygame.K_h: lambda: self.pygame_view.toggle_visibility("controls"),
            pygame.K_F5: lambda: self.game_world.handle_save(),
            pygame.K_F6: lambda: self.handle_load()
        }

        self.font = pygame.font.Font(None, 18)
        self.win_message = None

    def handle_load(self):
        self.game_world.handle_load()
        self.initialize()

    def initiate_combat(self):
        if self.debug_mode:
            return
        self.logger.debug("Initiating combat", stacklevel=2)
        self.combat_manager.reset_combat_state()  # Ensure we're in WAITING state
        self.pygame_view.room_items_display.is_visible = False
        self.pygame_view.minimap_visible = False
        self.pygame_view.controls_visible = False
        self.pygame_view.player_message_visible = False
        self.pygame_view.player_stats_visible = False
        self.combat_manager.trigger("start_combat")

    def handle_combat_end(self):
        if self.game_world.current_room.room.has_items:
            self.pygame_view.room_items_display.is_visible = True
        self.pygame_view.minimap_visible = True
        self.pygame_view.controls_visible = True
        self.pygame_view.player_stats_visible = True

    def load_and_play_music(self):
        try:
            pygame.mixer.music.load(RESOURCES_DIR + "/dungeon_adventure.wav")
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            self.logger.error(f"Error loading music: {e}")

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
        clock = pygame.time.Clock()
        while running:
            time_delta = clock.tick(60) / 1000.0
            running = self.handle_events()

            if self.game_world.game_model.game_state != GameState.GAME_OVER:
                self.update(time_delta)

            self.draw()
            pygame.display.flip()

        self.logger.info("Game loop ended")
        pygame.quit()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                self.logger.info("Quit event received")
                return False
            if self.game_world.game_model.game_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                        return True
                    elif event.key == pygame.K_q:
                        return False
            # Right now this is being called directly from game controller,
            # maybe we can do it through combat manager instead.
            # self.combat_screen.handle_event(event)
            self._handle_inventory_events(event)
            self._handle_keydown_event(event)
            self._handle_combat_events(event)
        return True

    def show_room_items(self):
        if (
            self.game_world.current_room.room.has_items
            and self.game_world.game_model.game_state != GameState.IN_COMBAT
        ):
            self.pygame_view.room_items_visible = True
        else:
            self.pygame_view.room_items_visible = False

    def _handle_keydown_event(self, event: pygame.event.Event) -> None:
        """Handle keydown events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                self.debug_mode = not self.debug_mode
            action = self.key_actions.get(event.key)
            if action:
                action()

    def _handle_combat_events(self, event: pygame.event.Event) -> None:
        """Handle combat and inventory-specific events."""
        self.combat_manager.process_events(event)
        # if self.combat_manager.enable_input_receiving:
        #     self.combat_manager.wait_for_user_input(event)

    def _handle_inventory_events(self, event: pygame.event.Event) -> None:
        if self.pygame_view.inventory_visible:
            self.pygame_view.handle_event(
                event, self.game_world.composite_player.player
            )

    def handle_room_enter(self):
        if self.debug_mode:
            return
        if (
            self.pygame_view.player_message_visible
            and self.game_world.current_room.room.room_type != RoomType.PIT
        ):
            self.pygame_view.player_message_visible = False

    def handle_pit_encounter(self):
        if self.debug_mode:
            return
        self.pygame_view.player_message_visible = True
        self.pygame_view.player_message_display.set_message(
            "Oh no! This room has a spike trap! You've taken damage."
        )
        if not self.game_world.composite_player.player.hero.is_alive:
            self.lose_condition = True
            self.handle_win_condition()

    def update(self, dt: float) -> None:
        self.game_world.update(dt)
        self.pygame_view.update(
            self.game_world.current_room,
            self.game_world.room_dict,
            self.game_world.composite_player.player,
        )
        self.debug_manager.update_fps(self.game_screen.clock)
        if self.game_world.game_model.game_state == GameState.IN_COMBAT:
            self.combat_manager.update(dt)
        self.combat_manager.update(dt)

    def draw(self) -> None:
        if (
            self.game_world.game_model.game_state == GameState.GAME_OVER
            and self.win_message
        ):
            self.game_screen.get_game_surface().fill((0, 0, 0))  # Clear screen
            for i, line in enumerate(self.win_message):
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(
                    center=(
                        self.game_screen.width // 2,
                        self.game_screen.height // 2 + i * 40,
                    )
                )
                self.game_screen.get_game_surface().blit(text_surface, text_rect)
        else:
            self.game_screen.draw_background()
            self._draw_game_world()
            self._draw_debug_info()
            self.game_screen.blit_scaled()
            if (
                self.game_world.game_model.game_state == GameState.IN_COMBAT
                and not self.debug_mode
            ):
                self._draw_combat_screen()
            self._draw_gui()
        if self.game_world.game_model.game_state == GameState.GAME_OVER:
            self.game_screen.blit_scaled()

    def _draw_combat_screen(self) -> None:
        self.combat_screen.draw(self.screen)

    def _draw_game_world(self) -> None:
        self.game_world.draw(self.game_screen.get_game_surface())

    def _draw_debug_info(self) -> None:
        if self.debug_manager.debug_mode:
            self.game_world.composite_player.py_player.draw_debug_info(
                self.game_screen.get_game_surface()
            )
            self.game_world.draw_debug(self.game_screen.get_game_surface())
            self.debug_manager.draw_debug_info(
                self.game_screen.get_game_surface(), self.game_world
            )

    def _draw_gui(self) -> None:
        if not self.debug_manager.debug_mode:
            self.pygame_view.draw(self.screen, self.game_world.composite_player.player)

    def handle_win_condition(self):
        if self.game_world.composite_player.hero.is_alive:
            self.logger.info("Win condition met! Player has collected all pillars.")
            self.win_message = [
                "Congratulations! You've collected all pillars and won the game!",
                "Press 'R' to restart or 'Q' to quit.",
            ]
        else:
            self.logger.info("Lose condition met! Player was defeated.")
            self.win_message = [
                "Game Over! You have been defeated.",
                "Press 'R' to restart or 'Q' to quit.",
            ]
        self.game_world.game_model.game_state = GameState.GAME_OVER

    def restart_game(self):
        # TODO: Still need to empty out the player inventory
        core_player = Player("Player 1", 50)
        py_player = PyPlayer()
        player = CompositePlayer(core_player, py_player)
        dungeon = DungeonGenerator.generate_default_dungeon()
        game_model = GameModel(core_player, dungeon)
        self.game_world = GameWorld(game_model, player)
        self.game_world.initialize()
        self.pygame_view.minimap_visible = True
        self.pygame_view.controls_visible = True
        self.pygame_view.player_stats_visible = True
        self.pygame_view.player_message_visible = False
        self.game_world.game_model.game_state = GameState.EXPLORING
        self.combat_manager.reset_combat_state()
        self.win_message = None
