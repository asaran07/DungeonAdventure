import logging
from typing import Callable, Dict, List, Optional

import pygame

from dungeon_adventure.enums.combat_state import CombatState
from dungeon_adventure.models.characters.hero import Hero
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.views.pygame.combat.combat_screen import (
    CombatAction,
    CombatScreen,
)
from dungeon_adventure.views.pygame.game.game_world import GameWorld
from dungeon_adventure.views.pygame.sprites.composite_player import CompositePlayer


class CombatManager:
    def __init__(self, game_world: GameWorld):
        self.enable_input_receiving: bool = False
        self.logger: logging.Logger = logging.getLogger("dungeon_adventure.combat")
        self.game_world: GameWorld = game_world
        self.view: Optional[CombatScreen] = None
        self.player: 'CompositePlayer' = game_world.composite_player
        self.monsters: List[Monster] = []
        self.combat_state: CombatState = CombatState.WAITING
        self.turn_order: List[Hero | Monster] = []
        self.current_turn_index: int = 0
        self.action_callbacks: Dict[CombatAction, Callable] = {
            CombatAction.ATTACK: self.handle_attack,
            CombatAction.FLEE: self.handle_flee,
            CombatAction.USE_ITEM: self.handle_use_item,
        }

    def set_combat_screen(self, combat_screen: CombatScreen) -> None:
        self.logger.info("Initializing combat screen")
        self.view = combat_screen

    def start_combat(self) -> None:
        self.logger.info("Starting combat")
        self.setup_combat()

    def setup_combat(self) -> None:
        self.logger.info("Setting up combat")
        self.monsters = self.game_world.current_room.room.monsters
        self.determine_turn_order()
        self.display_combat_info()

    def determine_turn_order(self) -> None:
        self.logger.info("Determining turn order")
        self.turn_order = [self.player.hero] + self.monsters
        self.turn_order.sort(key=lambda x: x.attack_speed, reverse=True)
        self.current_turn_index = 0
        self.logger.debug(f"Turn order: {[char.name for char in self.turn_order]}")

    def display_combat_info(self) -> None:
        if self.view:
            self.view.set_message("Combat Started!", self.on_setup_message_complete)
        else:
            self.logger.warning("Combat screen not initialized")

    def on_setup_message_complete(self) -> None:
        self.logger.debug("Setup message display completed")
        if self.view:
            self.view.display_stat_bars(
                self.player, True, True, True, self.on_stat_bars_displayed
            )
            self.view.display_monster_stats(self.monsters, self.on_monster_stats_displayed)
        self.start_next_turn()

    def on_stat_bars_displayed(self) -> None:
        self.logger.debug("Player stat bars displayed")

    def on_monster_stats_displayed(self) -> None:
        self.logger.debug("Monster stats displayed")

    def start_next_turn(self) -> None:
        current_character = self.turn_order[self.current_turn_index]
        self.logger.info(f"Starting turn for {current_character.name}")
        if isinstance(current_character, Hero):
            self.start_player_turn()
        else:
            self.start_monster_turn(current_character)

    def start_player_turn(self) -> None:
        self.logger.info("Starting player turn")
        if self.view:
            self.view.set_message("Your turn! Choose an action.", None)
        # Enable player input

    def start_monster_turn(self, monster: Monster) -> None:
        self.logger.info(f"Starting turn for {monster.name}")
        # Implement monster AI here
        self.end_turn()

    def handle_attack(self, monster_index: int) -> None:
        if 0 <= monster_index < len(self.monsters):
            target = self.monsters[monster_index]
            self.logger.info(f"Player attacking {target.name}")
            attack_amount = self.player.hero.attempt_attack(target)
            if attack_amount == 0:
                self.logger.info(f"{self.player.hero.name} missed attack on {target.name}")
            else:
                self.logger.info(f"{self.player.hero.name} attacked {target.name} for {attack_amount} damage")
            self.end_turn()
        else:
            self.logger.warning(f"Invalid monster index: {monster_index}")

    def handle_flee(self) -> None:
        self.logger.info("Player chose to flee")
        # Implement flee logic here

    def handle_use_item(self) -> None:
        self.logger.info("Player chose to use an item")
        # Implement item use logic here
        self.end_turn()

    def update(self, dt: float) -> None:
        if self.view:
            self.view.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        if self.view:
            self.view.draw(surface)

    def process_events(self, event: pygame.event.Event) -> None:
        if self.view:
            action = self.view.handle_event(event)
            if isinstance(action, tuple) and action[0] == "ATTACK":
                self.logger.info(f"Attacking monster at index {action[1]}")
                self.handle_attack(action[1])
            elif action == CombatAction.FLEE:
                self.handle_flee()
            elif action == CombatAction.USE_ITEM:
                self.handle_use_item()
        else:
            self.logger.warning("Combat screen not initialized")

    def wait_for_user_input(self, event: pygame.event.Event) -> None:
        pass

    def end_turn(self) -> None:
        self.logger.info("Ending turn")
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        self.start_next_turn()

    def update_combat_display(self) -> None:
        if self.view:
            self.view.update_stat_bars(self.player, self.on_stat_bars_updated)
            self.view.update_monster_stats(self.monsters, self.on_monster_stats_updated)

    def on_stat_bars_updated(self) -> None:
        self.logger.debug("Player stat bars updated")

    def on_monster_stats_updated(self) -> None:
        self.logger.debug("Monster stats updated")