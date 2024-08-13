import logging
from enum import Enum
from typing import List, Optional

import pygame
from transitions import Machine

from dungeon_adventure.enums.combat_state import CombatState
from dungeon_adventure.enums.game_state import GameState
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
        self.waiting_for_animation = None
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
        self.machine.add_transition(
            "end_combat",
            States.PLAYER_TURN,
            States.COMBAT_END,
            before="handle_combat_end"
        )
        self.machine.add_transition(
            "start_monster_turn",
            States.PLAYER_TURN,
            States.MONSTER_TURN,
            after="handle_monster_turn"
        )
        self.machine.add_transition(
            "end_monster_turn",
            States.MONSTER_TURN,
            States.PLAYER_TURN,
            after="start_player_turn"
        )
        self.machine.add_transition(
            'start_combat',
            [States.WAITING, States.COMBAT_END],  # Allow starting from COMBAT_END too
            States.PLAYER_TURN,
            before='setup_combat',
            after='start_player_turn'
        )
        self.machine.add_transition(
            'reset_combat',
            '*',  # Allow resetting from any state
            States.WAITING
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
        if self.state == States.PLAYER_TURN and self.view and not self.waiting_for_animation:
            action = self.view.handle_event(event)
            if isinstance(action, tuple) and action[0] == "ATTACK":
                self.logger.info(f"Attacking monster at index {action[1]}")
                self.handle_attack(action[1])
            elif action == CombatAction.FLEE:
                # Implement flee logic
                pass
            elif action == CombatAction.USE_ITEM:
                # Implement use item logic
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
        self.waiting_for_animation = False

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

            self.waiting_for_animation = True
            if attack_amount == 0:
                self.logger.info(f"{self.player.hero.name} missed attack on {target.name}")
                self.view.set_message("You missed!", self.on_attack_animation_complete)
            else:
                self.logger.info(f"{self.player.hero.name} attacked {target.name} for {attack_amount} damage")
                self.view.set_message(f"You hit {target.name} for {attack_amount} damage!",
                                      self.on_attack_animation_complete)
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
        if self.player.hero.current_hp <= 0:
            self.logger.info("Player has been defeated. Ending combat.")
            self.end_combat()
        elif all(monster.current_hp <= 0 for monster in self.monsters):
            self.logger.info("All monsters defeated. Ending combat.")
            self.end_combat()
        else:
            self.logger.debug("Combat continues.")

    def on_attack_animation_complete(self):
        self.waiting_for_animation = False
        self.check_combat_end()
        if self.state != States.COMBAT_END:
            self.start_monster_turn()

    def handle_combat_end(self):
        self.logger.info("Combat has ended. Transitioning to post-combat state.")
        if self.player.hero.current_hp <= 0:
            if self.view:
                self.view.set_message("Game Over! You have been defeated.", self.transition_to_game_over)
            else:
                self.transition_to_game_over()
        else:
            if self.view:
                self.view.set_message("Victory! All monsters defeated.", self.transition_to_exploration)
            else:
                self.transition_to_exploration()

    def transition_to_game_over(self):
        self.logger.info("Transitioning to game over screen.")
        self.game_world.game_model.set_game_over(True)

    def transition_to_exploration(self):
        self.logger.info("Transitioning back to exploration mode.")
        self.game_world.game_model.game_state = GameState.EXPLORING
        self.reset_combat_state()

    def handle_monster_turn(self):
        self.logger.info("CURRENT STATE: " + str(self.state))
        self.logger.info("Starting monster turn")
        self.waiting_for_animation = True
        self.process_monster_attacks()

    def process_monster_attacks(self):
        self.current_monster_index = 0
        self.process_next_monster_attack()

    def process_next_monster_attack(self):
        if self.current_monster_index < len(self.monsters):
            monster = self.monsters[self.current_monster_index]
            if monster.current_hp > 0:
                attack_amount = monster.attempt_attack(self.player.hero)
                if attack_amount == 0:
                    self.logger.info(f"{monster.name} missed attack on {self.player.hero.name}")
                    self.view.set_message(f"{monster.name} missed!", self.on_monster_attack_complete)
                else:
                    self.logger.info(f"{monster.name} attacked {self.player.hero.name} for {attack_amount} damage")
                    self.view.set_message(f"{monster.name} hit you for {attack_amount} damage!",
                                          self.on_monster_attack_complete)
            else:
                self.on_monster_attack_complete()
        else:
            self.on_all_monster_attacks_complete()

    def on_monster_attack_complete(self):
        self.current_monster_index += 1
        self.process_next_monster_attack()

    def on_all_monster_attacks_complete(self):
        self.waiting_for_animation = False
        self.check_combat_end()
        if self.state != States.COMBAT_END:
            self.end_monster_turn()

    def reset_combat_state(self):
        self.logger.info("Resetting combat state to WAITING")
        if self.state != States.WAITING:
            self.trigger('reset_combat')
        self.monsters = []
        self.turn_order = []
        self.waiting_for_animation = False
        self.message_animation_complete = False







