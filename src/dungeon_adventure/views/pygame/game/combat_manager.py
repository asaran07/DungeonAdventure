import logging
from enum import Enum
from typing import List, Optional

import pygame
from transitions import Machine

from dungeon_adventure.enums.combat_state import CombatState
from dungeon_adventure.models.characters.hero import Hero
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.views.pygame.combat.combat_screen import (
    CombatAction,
    CombatScreen,
)
from dungeon_adventure.views.pygame.game.game_world import GameWorld
from dungeon_adventure.views.pygame.sprites.composite_player import CompositePlayer


class States(Enum):
    WAITING = "waiting"
    PLAYER_TURN = "player_turn"
    MONSTER_TURN = "monster_turn"
    ANIMATING = "animating"
    COMBAT_END = "combat_end"


class CombatManager:
    def __init__(self, game_world: GameWorld):
        self.enable_input_receiving: bool = False
        self.logger: logging.Logger = logging.getLogger("dungeon_adventure.combat")
        self.game_world: GameWorld = game_world
        self.view: Optional[CombatScreen] = None
        self.player: "CompositePlayer" = game_world.composite_player
        self.monsters: List[Monster] = []
        self.combat_state: CombatState = CombatState.WAITING
        self.turn_order: List[Hero | Monster] = []
        self.message_animation_complete = False

        # Initialize the state machine
        self.machine: Machine = Machine(
            model=self, states=States, initial=States.WAITING
        )

        # Define transitions
        self.machine.add_transition(
            "start_combat",
            States.WAITING,
            States.PLAYER_TURN,
            before="setup_combat",
            after="start_player_turn",
        )

    def set_combat_screen(self, combat_screen: CombatScreen) -> None:
        self.logger.info("CURRENT STATE: " + str(self.state))
        self.logger.info("Initializing combat screen")
        self.view = combat_screen

    def setup_combat(self) -> None:
        self.logger.info("CURRENT STATE: " + str(self.state))
        self.logger.info("Setting up combat")
        self.monsters = self.game_world.current_room.room.monsters
        self.determine_turn_order()
        self.display_combat_info()
        # Wait for animation to complete before allowing the transition
        self.wait_for_animation()

    def wait_for_animation(self):
        if not self.message_animation_complete:
            # If the animation isn't complete, check again after a short delay
            pygame.time.set_timer(pygame.USEREVENT, 100)  # Check every 100ms

    def determine_turn_order(self) -> None:
        self.logger.info("CURRENT STATE: " + str(self.state))
        self.logger.info("Determining turn order")
        self.turn_order = [self.player.hero] + self.monsters
        self.turn_order.sort(key=lambda x: x.attack_speed, reverse=True)
        self.logger.debug(f"Turn order: {[char.name for char in self.turn_order]}")

    def display_combat_info(self) -> None:
        self.logger.info("CURRENT STATE: " + str(self.state))
        self.logger.info("Displaying turn order")
        if self.view:
            self.message_animation_complete = False
            self.view.set_message("Combat Started!", self.on_message_complete)
        else:
            self.logger.warning("Combat screen not initialized")

    def on_message_complete(self) -> None:
        self.message_animation_complete = True
        self.logger.info("Message animation complete")
        # Manually trigger the state transition
        self.to_PLAYER_TURN()

    def process_events(self, event):
        if event.type == pygame.USEREVENT:
            if self.message_animation_complete:
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer
                self.to_PLAYER_TURN()
            else:
                self.wait_for_animation()
        if self.state == States.PLAYER_TURN and self.view:
            action = self.view.handle_event(event)
            if isinstance(action, tuple) and action[0] == "ATTACK":
                self.logger.info(f"Attacking monster at index {action[1]}")
                self.handle_attack(action[1])
            elif action == CombatAction.FLEE:
                pass
            elif action == CombatAction.USE_ITEM:
                pass

    def start_player_turn(self) -> None:
        self.logger.info("CURRENT STATE: " + str(self.state))
        self.logger.info("Starting player turn")
        if self.view:
            self.view.display_stat_bars(
                self.player, True, True, True, self.on_stat_bars_displayed
            )
        else:
            self.logger.error("View is None in start_player_turn")

    def on_stat_bars_displayed(self) -> None:
        # self.logger.debug("Player stat bars displayed")
        if self.view:
            self.view.display_monster_stats(
                self.monsters, self.on_monster_stats_displayed
            )
        else:
            self.logger.error("View is None in on_stat_bars_displayed")

    def on_monster_stats_displayed(self) -> None:
        self.logger.debug("Monster stats displayed")
        if self.view:
            self.view.set_message("Your turn! Choose an action.", None)

    def handle_attack(self, monster_index: int) -> None:
        self.logger.info("CURRENT STATE: " + str(self.state))
        if 0 <= monster_index < len(self.monsters):
            target = self.monsters[monster_index]
            self.logger.info(f"Player attacking {target.name}")
            attack_amount = self.player.hero.attempt_attack(target)
            if attack_amount == 0:
                self.logger.info(
                    f"{self.player.hero.name} missed attack on {target.name}"
                )
                self.view.set_message("You missed!", self.check_combat_end)
            else:
                self.logger.info(
                    f"{self.player.hero.name} attacked {target.name} for {attack_amount} damage"
                )
                self.view.set_message(
                    f"You hit {target.name} for {attack_amount} damage!", self.check_combat_end
                )
        else:
            self.logger.warning(f"Invalid monster index: {monster_index}")

    def draw(self, surface: pygame.Surface) -> None:
        if self.view:
            self.view.draw(surface)

    def update(self, dt: float) -> None:
        if self.view:
            self.view.update(dt)

    def check_combat_end(self):
        self.logger.debug("Checking combat end...")
        self.logger.debug(f"Monster 1 and 2 hp: {self.monsters[0].current_hp, self.monsters[1].current_hp}")


    # def prepare_monster_turn(self):
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.info("Preparing monster turn")
    #     current_monster = self.turn_order[self.current_turn_index]
    #     self.handle_monster_action(current_monster)
    #
    # def handle_monster_action(self, monster: Monster) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     target = self.player.hero
    #     attack_amount = monster.attempt_attack(target)
    #     if attack_amount == 0:
    #         self.view.set_message(f"{monster.name} missed!", self.end_monster_turn)
    #     else:
    #         self.view.set_message(
    #             f"{monster.name} hit you for {attack_amount} damage!",
    #             self.end_monster_turn,
    #         )
    #         self.view.update_stat_bars(self.player, self.on_stat_bars_updated)

    # def prepare_player_turn(self):
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.info("Preparing player turn")
    #     if self.view:
    #         self.view.set_message("Your turn! Choose an action.", None)
    #
    # def start_next_turn(self) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     current_character = self.turn_order[self.current_turn_index]
    #     self.logger.info(f"Starting turn for {current_character.name}")
    #     if isinstance(current_character, Hero):
    #         self.start_player_turn()
    #     else:
    #         self.start_monster_turn(current_character)

    # def start_monster_turn(self, monster: Monster) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.info(f"Starting turn for {monster.name}")
    #     # Implement monster AI here
    #     self.end_turn()

    # def handle_flee(self) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.info("Player chose to flee")
    #     # Implement flee logic here
    #
    # def handle_use_item(self) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.info("Player chose to use an item")
    #     # Implement item use logic here
    #     self.end_turn()

    #
    # if self.state == "animating":
    #     current_time = pygame.time.get_ticks()
    #     if current_time - self.animation_timer >= self.animation_duration:
    #         if isinstance(self.turn_order[self.current_turn_index], Hero):
    #             self.start_player_turn()
    #         else:
    #             self.start_monster_turn()

    #
    # def wait_for_user_input(self, event: pygame.event.Event) -> None:
    #     pass
    #
    # def end_turn(self) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.info("Ending turn")
    #     self.start_next_turn()
    #
    # def update_combat_display(self) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     if self.view:
    #         self.view.update_stat_bars(self.player, self.on_stat_bars_updated)
    #         self.view.update_monster_stats(self.monsters, self.on_monster_stats_updated)
    #
    # def on_stat_bars_updated(self) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.debug("Player stat bars updated")
    #
    # def on_monster_stats_updated(self) -> None:
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.debug("Monster stats updated")
    #
    # def cleanup_combat(self):
    #     self.logger.info("CURRENT STATE: " + self.state)
    #     self.logger.info("Combat ended")
