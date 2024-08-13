import logging
from typing import Callable, List, Optional

import pygame
from transitions import Machine

from dungeon_adventure.enums.combat_state import CombatState
from dungeon_adventure.models.characters.hero import Hero
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.views.pygame.combat.combat_screen import CombatScreen
from dungeon_adventure.views.pygame.game.game_world import GameWorld


class CombatManager:
    states = [
        "idle",
        "setup",
        "player_turn",
        "enemy_turn",
        "animating_attack",
        "combat_end",
    ]

    def __init__(self, game_world: GameWorld):
        self.logger = logging.getLogger("dungeon_adventure.combat")
        self.elapsed_log_time = 0
        self.log_interval = 5000  # Log every 5000 milliseconds (5 seconds)
        self.combat_time = 0  # Track total combat time

        self.enable_input_receiving = False
        self.game_world = game_world
        self.view: CombatScreen = Optional[None]
        self.player = game_world.composite_player
        self.monsters: List[Monster] = []
        self.combat_state: CombatState = CombatState.WAITING
        self.current_turn: int = 0
        self.turn_order: List[Hero | Monster] = []
        self.selected_monster: Optional[Monster] = None
        self.available_actions: List[str] = ["Attack", "Use Item", "Flee"]
        self.total_xp_gained: int = 0
        self.monsters_defeated: int = 0
        self.combat_over: bool = False
        self.current_action = ""

        self.machine = Machine(model=self, states=CombatManager.states, initial="idle")
        self.machine.add_transition(
            "start_combat", "idle", "setup", after="setup_combat"
        )
        self.machine.add_transition(
            "setup_complete", "setup", "player_turn", after="start_player_turn"
        )
        self.machine.add_transition(
            "player_action",
            "player_turn",
            "animating_attack",
            after="handle_player_action",
        )
        self.machine.add_transition(
            "animation_complete",
            "animating_attack",
            "enemy_turn",
            after="start_enemy_turn",
        )
        self.machine.add_transition(
            "enemy_action",
            "enemy_turn",
            "animating_attack",
            after="handle_enemy_action",
        )
        self.machine.add_transition(
            "turn_complete",
            "animating_attack",
            "player_turn",
            conditions=["combat_active"],
            after="start_player_turn",
        )
        self.machine.add_transition(
            "turn_complete",
            "animating_attack",
            "combat_end",
            conditions=["combat_over"],
            after="end_combat",
        )

    def set_combat_screen(self, combat_screen: CombatScreen):
        self.logger.info("Initializing combat screen")
        self.view = combat_screen
        # self.setup_action_callbacks()

    #
    # def setup_action_callbacks(self):
    #     if self.view:
    #         self.view.set_action_callback("attack", self.handle_attack)
    #         self.view.set_action_callback("use_item", self.handle_use_item)
    #         self.view.set_action_callback("flee", self.handle_flee)

    def process_events(self, event: pygame.event.Event):
        pass
        # if self.view:
        #     self.view.process_events(event)
        # else:
        #     self.logger.warning("Combat screen not initialized")

    def setup_combat(self):
        self.logger.info("Setting up combat")
        self.monsters = self.game_world.current_room.room.monsters
        self.determine_turn_order()
        if self.view:
            self.logger.debug("Connecting to combat screen")
            self.view.set_message("Combat Started!", self.on_setup_message_complete)
        # self.update_combat_screen()

    def on_stat_bars_displayed(self):
        self.logger.debug("Stats bars creation finished")

    def on_setup_message_complete(self):
        self.logger.debug("Setup message complete callback from combat_screen received!", stacklevel=2)
        self.setup_complete()

    def determine_turn_order(self) -> None:
        self.logger.info("Determining turn order")
        self.turn_order = [self.player.hero] + self.monsters
        self.turn_order.sort(key=lambda x: x.attack_speed, reverse=True)

    def handle_attack(self):
        self.logger.info("Attack action triggered")
        self.player_action()

    def handle_use_item(self):
        self.logger.info("Use Item action triggered")
        self.player_action()

    def handle_flee(self):
        self.logger.info("Flee action triggered")
        self.player_action()

    def handle_player_action(self):
        # Implement player action logic here
        if self.view:
            self.view.set_message("You attack!", self.on_player_action_complete)

    def on_player_action_complete(self):
        self.animation_complete()

    def start_player_turn(self):
        self.logger.info("Starting Player Turn")
        self.view.display_stat_bars(
            self.player, True, True, True, self.on_stat_bars_displayed
        )
        if self.current_turn < len(self.turn_order):
            character = self.turn_order[self.current_turn]
            self.logger.info(f"Turn starting for {character}")

    def start_enemy_turn(self):
        self.logger.info("Starting enemy turn")
        # Implement enemy turn logic here
        self.enemy_action()

    def handle_enemy_action(self):
        # Implement enemy action logic here
        if self.view:
            self.view.set_message("Enemy attacks!", self.on_enemy_action_complete)

    def on_enemy_action_complete(self):
        self.turn_complete()

    def combat_active(self):
        return len(self.monsters) > 0 and self.player.hero.is_alive

    def combat_over(self):
        return not self.combat_active()

    def end_combat(self):
        self.logger.info("Combat ended")
        if self.view:
            self.view.set_message("Combat ended!", self.on_combat_end_complete)

    def on_combat_end_complete(self):
        # Implement post-combat cleanup here
        pass

    def wait_for_user_input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.logger.debug("Keypress detected")
            if event.key == pygame.K_TAB:
                self.logger.debug("Tab key pressed")

    def update(self, dt):
        self.combat_time += dt

        current_time = pygame.time.get_ticks()
        if current_time - self.elapsed_log_time > self.log_interval:
            self.logger.debug(
                f"Updating combat state (dt: {dt:.2f}ms, total combat time: {self.combat_time:.2f}ms)"
            )
            self.elapsed_log_time = current_time

        if self.view:
            self.view.update(dt)

    def draw(self, surface):
        self.view.draw(surface)
