import logging
from typing import List, Optional

import pygame
from transitions import Machine

from dungeon_adventure.enums.combat_state import CombatState
from dungeon_adventure.models.characters.hero import Hero
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.views.pygame.combat.combat_screen import CombatScreen
from dungeon_adventure.views.pygame.game.game_world import GameWorld


class CombatManager:
    states = ["idle", "player_turn", "enemy_turn", "animating_attack", "combat_end"]

    def __init__(self, game_world: GameWorld):
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
        self.logger = logging.getLogger("dungeon_adventure.combat")

        self.machine = Machine(model=self, states=CombatManager.states, initial="idle")
        self.machine.add_transition(
            "start_combat", "idle", "player_turn", after="setup_combat"
        )
        self.machine.add_transition(
            "end_player_turn", "player_turn", "enemy_turn", after="start_enemy_turn"
        )
        self.machine.add_transition(
            "start_attack_animation",
            "*",
            "animating_attack",
            after="play_attack_animation",
        )
        self.machine.add_transition(
            "end_attack_animation", "animating_attack", "=", after="resolve_attack"
        )
        self.machine.add_transition(
            "end_combat", "*", "combat_end", after="cleanup_combat"
        )

    def set_combat_screen(self, combat_screen: CombatScreen):
        self.view = combat_screen
        self.setup_action_callbacks()

    def setup_action_callbacks(self):
        if self.view:
            self.view.set_action_callback("attack", self.handle_attack)
            self.view.set_action_callback("use_item", self.handle_use_item)
            self.view.set_action_callback("flee", self.handle_flee)

    def handle_attack(self):
        self.logger.info("Attack action triggered")
        # Implement attack logic here

    def handle_use_item(self):
        self.logger.info("Use Item action triggered")
        # Implement use item logic here

    def handle_flee(self):
        self.logger.info("Flee action triggered")
        # Implement flee logic here

    def process_events(self, event: pygame.event.Event):
        if self.view:
            self.view.process_events(event)
        else:
            self.logger.warning("Combat screen not initialized")

    def setup_combat(self):
        self.logger.info("Setting up combat")
        self.determine_turn_order()
        self.update_combat_screen()

    def determine_turn_order(self) -> None:
        self.logger.info("Determining turn order")
        self.turn_order = [self.player.hero] + self.monsters
        self.turn_order.sort(key=lambda x: x.attack_speed, reverse=True)

    def update_combat_screen(self):
        self.logger.info("Updating combat screen")
        if self.view:
            self.view.update_player_info(
                self.player.hero.current_hp, self.player.hero.max_hp
            )
            self.view.display_combat_message("Monsters encountered!")
            self.logger.info("Start waiting for user input")
            self.enable_input_receiving = True

    def wait_for_user_input(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.logger.debug("Keypress detected")
            if event.key == pygame.K_TAB:
                self.logger.debug("Tab key pressed")
                self.cycle_action_choices()

    def cycle_action_choices(self):
        self.logger.info(
            "Cycling action choices, current action: {}".format(self.current_action)
        )
        if self.current_action == "":
            self.view.clear_action_display()
            self.view.draw_on_action_display("Attack")
            self.current_action = "Attack"
        elif self.current_action == "Attack":
            self.view.clear_action_display()
            self.view.draw_on_action_display("Flee")
            self.current_action = "Flee"
        elif self.current_action == "Flee":
            self.view.clear_action_display()
            self.view.draw_on_action_display("Use Item")
            self.current_action = "Use Item"
        elif self.current_action == "Use Item":
            self.view.clear_action_display()
            self.view.draw_on_action_display("Action")
            self.current_action = ""
        else:
            self.view.clear_action_display()
            self.logger.warning("Invalid action choice")

    def start_enemy_turn(self):
        print("Enemy turn starting...")

    def play_attack_animation(self):
        print("Playing attack animation...")

    def resolve_attack(self):
        print("Resolving attack...")

    def cleanup_combat(self):
        print("Cleaning up after combat...")

    def update(self, dt):
        self.view.update(dt)

    def draw(self, surface):
        self.view.draw(surface)

    # def handle_event(self, event: pygame.event.Event):
    #     # We don't process any events unless we're ready for input
    #     # (so if we've already done the pre combat preparations)
    #     if CombatState == CombatState.READY:
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_a:
    #                 return self.handle_combat_action("Attack")
    #             elif event.key == pygame.K_u:
    #                 return self.handle_combat_action("Use Item")
    #             elif event.key == pygame.K_f:
    #                 return self.handle_combat_action("Flee")

    # def initiate_combat(self) -> None:
    #     self.logger.info("Initiating combat")
    #     self.monsters = self.game_world.current_room.room.monsters
    #     if not self.monsters:
    #         self.logger.warning("No monsters found while initializing combat")
    #         return
    #     self.game_world.game_model.game_state = GameState.IN_COMBAT
    #     self.combat_state = CombatState.PLAYER_TURN

    #
    # def handle_combat_action(
    #     self, action: str, target_index: Optional[int] = None
    # ) -> str:
    #     if action == "Attack":
    #         return self.handle_attack(target_index)
    #     elif action == "Use Item":
    #         return "Item use not implemented yet."
    #     elif action == "Flee":
    #         return self.attempt_flee()
    #     else:
    #         return "Invalid action."

    # def handle_attack(self, target_index: Optional[int]) -> str:
    #     if target_index is None or target_index >= len(self.monsters):
    #         return "Invalid target."
    #     target = self.monsters[target_index]
    #     damage = self.player.hero.attempt_attack(target)
    #     message = f"You deal {damage} damage to {target.name}!"
    #     if not target.is_alive:
    #         message += f" {target.name} has been defeated!"
    #         self.monsters.pop(target_index)
    #     return message
    #
    # def attempt_flee(self) -> str:
    #     if random.random() < 0.5:
    #         self.end_combat()
    #         return "You successfully fled from combat!"
    #     else:
    #         return "Failed to flee. You lose your turn!"
    #
    # def handle_monster_turns(self) -> List[str]:
    #     messages = []
    #     for monster in self.monsters:
    #         damage = monster.attempt_attack(self.player.hero)
    #         messages.append(f"{monster.name} deals {damage} damage to you!")
    #     return messages
    #
    # def is_combat_over(self) -> bool:
    #     return not self.monsters or not self.player.hero.is_alive
    #
    # def end_combat(self) -> None:
    #     self.game_world.game_model.game_state = GameState.EXPLORING
    #     self.combat_state = CombatState.WAITING
    #     self.monsters = []
    #

    #
    # def handle_player_action(
    #     self, action: str, target_index: Optional[int] = None
    # ) -> str:
    #     self.logger.info("Handling player action")
    #     if action == "Attack":
    #         self.logger.debug(
    #             "Action -> Attack, attacking monster {}".format(target_index)
    #         )
    #         if target_index is not None and 0 <= target_index < len(self.monsters):
    #             return self.player_attack(self.monsters[target_index])
    #         else:
    #             return "Invalid target."
    #     elif action == "Use Item":
    #         return "Item use not implemented yet."
    #     elif action == "Flee":
    #         return self.attempt_flee()
    #     else:
    #         return "Invalid action."
    #
    # def player_attack(self, target: Monster) -> str:
    #     damage = self.player.hero.attempt_attack(target)
    #     self.logger.debug("Calculated damage = {}".format(damage))
    #     message = f"You deal {damage} damage to {target.name}!"
    #     if not target.is_alive:
    #         self.logger.debug("Monster {} defeated".format(target.name))
    #         self.handle_monster_defeat(target)
    #     self.next_turn()
    #     return message
    #
    # def handle_monster_defeat(self, monster: Monster) -> None:
    #     self.monsters.remove(monster)
    #     self.turn_order.remove(monster)
    #     xp_gained = monster.xp_reward
    #     self.player.hero.gain_xp(xp_gained)
    #     self.total_xp_gained += xp_gained
    #     self.monsters_defeated += 1
    #
    # def next_turn(self) -> None:
    #     self.logger.info("Advancing turn")
    #     if not self.turn_order:
    #         self.end_combat()
    #         return
    #
    #     self.current_turn = (self.current_turn + 1) % len(self.turn_order)
    #     if self.current_turn == 0:
    #         self.logger.debug("Switching to player turn state")
    #         self.combat_state = CombatState.PLAYER_TURN
    #     else:
    #         self.logger.debug("Switching to monster turn state")
    #         self.combat_state = CombatState.MONSTER_TURN
    #
    # def handle_monster_turn(self) -> str:
    #     self.logger.debug("Handling turn for monster {}".format(len(self.monsters)))
    #     monster = self.turn_order[self.current_turn]
    #     damage = monster.attempt_attack(self.player.hero)
    #     self.next_turn()
    #     return f"{monster.name} deals {damage} damage to you!"
    #
    # def get_combat_summary(self) -> dict:
    #     return {
    #         "monsters_defeated": self.monsters_defeated,
    #         "total_xp_gained": self.total_xp_gained,
    #         "player_hp": self.player.hero.current_hp,
    #         "player_max_hp": self.player.hero.max_hp,
    #         "monsters": [
    #             {"name": m.name, "hp": m.current_hp, "max_hp": m.max_hp}
    #             for m in self.monsters
    #         ],
    #     }
