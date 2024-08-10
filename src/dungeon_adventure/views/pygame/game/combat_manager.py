import random

import pygame
from typing import List, Optional
from dungeon_adventure.enums.combat_state import CombatState
from dungeon_adventure.enums.game_state import GameState
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.views.pygame.game.game_world import GameWorld


class CombatManager:
    def __init__(self, game_world: GameWorld):
        self.game_world = game_world
        self.player = game_world.composite_player
        self.monsters: List[Monster] = []
        self.combat_state = CombatState.WAITING
        self.current_turn = 0
        self.turn_order = []
        self.selected_monster: Optional[Monster] = None
        self.font = pygame.font.Font(None, 24)
        self.available_actions = ["Attack", "Use Item", "Flee"]
        self.action_index = 0
        self.monster_index = -1
        self.selection_mode = "action"  # Can be "action" or "monster"
        self.last_action_time = 0
        self.action_delay = 100  # 0.5 second delay between actions
        self.combat_message = ""
        self.combat_message_time = 0
        self.combat_message_duration = 2000  # 2 seconds to display combat messages

        self.combat_summary = ""
        self.combat_summary_time = 0
        self.combat_summary_duration = 5000  # 5 seconds to display the summary
        self.total_xp_gained = 0
        self.monsters_defeated = 0
        self.combat_over = False

    def initiate_combat(self):
        self.monsters = self.game_world.current_room.room.monsters
        if not self.monsters:
            return

        self.game_world.game_model.game_state = GameState.IN_COMBAT
        self.determine_turn_order()
        self.combat_state = CombatState.PLAYER_TURN
        self.current_turn = 0
        self.selected_monster = None
        self.action_index = 0
        self.monster_index = -1
        self.selection_mode = "action"

    def determine_turn_order(self):
        self.turn_order = [self.player.hero] + self.monsters
        self.turn_order.sort(key=lambda x: x.attack_speed, reverse=True)

    def update(self):
        if self.game_world.game_model.game_state != GameState.IN_COMBAT:
            return

        current_time = pygame.time.get_ticks()

        if self.combat_state == CombatState.SUMMARY:
            if current_time - self.combat_summary_time >= self.combat_summary_duration:
                self.end_combat("Combat has ended.")
            return

        # Handle combat message display
        if current_time - self.combat_message_time < self.combat_message_duration:
            return

        if self.combat_state == CombatState.MONSTER_TURN and current_time - self.last_action_time >= self.action_delay:
            if self.turn_order:
                self.handle_monster_turn(self.turn_order[self.current_turn])
            self.last_action_time = current_time

    def handle_monster_turn(self, monster: Monster):
        damage = monster.attempt_attack(self.player.hero)
        self.set_combat_message(f"{monster.name} deals {damage} damage to you!")
        self.next_turn()

    def player_attack(self):
        if self.selected_monster:
            damage = self.player.hero.attempt_attack(self.selected_monster)
            self.set_combat_message(f"You deal {damage} damage to {self.selected_monster.name}!")
            self.check_combat_end(self.selected_monster)
            if not self.combat_over:
                self.next_turn()
            self.reset_selection()

    def draw_combat_summary(self, surface: pygame.Surface):
        summary_lines = self.combat_summary.split('\n')
        for i, line in enumerate(summary_lines):
            summary_surface = self.font.render(line, True, (255, 255, 0))
            surface.blit(summary_surface, (10, 10 + i * 30))

    def next_turn(self):
        if not self.turn_order:  # If turn_order is empty, combat has ended
            self.end_combat("Combat has ended.")
            return

        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        if self.current_turn == 0:
            self.combat_state = CombatState.PLAYER_TURN
            self.reset_selection()
        else:
            self.combat_state = CombatState.MONSTER_TURN

    def reset_selection(self):
        self.selection_mode = "action"
        self.action_index = 0
        self.monster_index = -1
        self.selected_monster = None

    def check_combat_end(self, target: Monster):
        if not target.is_alive:
            self.monsters.remove(target)
            self.turn_order.remove(target)
            xp_gained = target.xp_reward
            self.player.hero.gain_xp(xp_gained)
            self.total_xp_gained += xp_gained
            self.monsters_defeated += 1
            self.set_combat_message(f"{target.name} has been defeated! You gained {xp_gained} XP.")

        if not self.monsters:
            self.combat_over = True
            self.display_combat_summary()
        elif not self.player.hero.is_alive:
            self.combat_over = True
            self.end_combat("Player has been defeated!")
            self.game_world.game_model.set_game_over(True)

    def display_combat_summary(self):
        self.combat_summary = (f"Combat Over!\n"
                               f"Monsters Defeated: {self.monsters_defeated}\n"
                               f"Total XP Gained: {self.total_xp_gained}\n"
                               f"Press ENTER to continue...")
        self.combat_summary_time = pygame.time.get_ticks()
        self.combat_state = CombatState.SUMMARY

    def end_combat(self, message: str):
        self.set_combat_message(message)
        self.game_world.game_model.game_state = GameState.EXPLORING
        self.combat_state = CombatState.WAITING
        self.monsters = []
        self.turn_order = []
        self.total_xp_gained = 0
        self.monsters_defeated = 0
        self.combat_over = False

    def set_combat_message(self, message: str):
        self.combat_message = message
        self.combat_message_time = pygame.time.get_ticks()

    def draw(self, surface: pygame.Surface):
        if self.game_world.game_model.game_state != GameState.IN_COMBAT:
            return

        if self.combat_state == CombatState.SUMMARY:
            self.draw_combat_summary(surface)
        else:
            # Draw player info
            player_text = f"Player HP: {self.player.hero.current_hp}/{self.player.hero.max_hp}"
            player_surface = self.font.render(player_text, True, (255, 255, 255))
            surface.blit(player_surface, (10, 10))

            # Draw available actions on a single line
            action_text = " | ".join(self.available_actions)
            action_surface = self.font.render(action_text, True, (255, 255, 255))
            surface.blit(action_surface, (10, 40))

            # Highlight the selected action
            if self.selection_mode == "action":
                start_pos = 10 + sum(
                    self.font.size(a)[0] + self.font.size(" | ")[0] for a in self.available_actions[:self.action_index])
                action_width = self.font.size(self.available_actions[self.action_index])[0]
                pygame.draw.rect(surface, (255, 255, 0), (start_pos, 38, action_width, 2))

            # Draw monsters
            for i, monster in enumerate(self.monsters):
                color = (255, 0, 0) if i == self.monster_index and self.selection_mode == "monster" else (255, 255, 255)
                monster_text = f"{monster.name} - HP: {monster.current_hp}/{monster.max_hp}"
                monster_surface = self.font.render(monster_text, True, color)
                surface.blit(monster_surface, (10, 70 + i * 30))

            # Draw combat message
            if pygame.time.get_ticks() - self.combat_message_time < self.combat_message_duration:
                message_surface = self.font.render(self.combat_message, True, (255, 255, 0))
                surface.blit(message_surface, (10, surface.get_height() - 90))

            # Draw combat state and instructions
            state_text = f"Combat State: {self.combat_state.name}"
            state_surface = self.font.render(state_text, True, (255, 255, 255))
            surface.blit(state_surface, (10, surface.get_height() - 60))

            instruction_text = "TAB: cycle actions, RIGHT ARROW: cycle monsters, ENTER: confirm"
            instruction_surface = self.font.render(instruction_text, True, (255, 255, 255))
            surface.blit(instruction_surface, (10, surface.get_height() - 30))

    def handle_event(self, event: pygame.event.Event):
        if self.combat_state == CombatState.SUMMARY:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.end_combat("Combat has ended.")
            return

        if self.combat_state != CombatState.PLAYER_TURN or self.combat_over:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_action_time < self.action_delay:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.cycle_action()
            elif event.key == pygame.K_RIGHT:
                self.cycle_monster()
            elif event.key == pygame.K_RETURN:
                self.confirm_selection()

        self.last_action_time = current_time

    def cycle_action(self):
        if self.selection_mode == "action":
            self.action_index = (self.action_index + 1) % len(self.available_actions)

    def cycle_monster(self):
        if self.selection_mode == "monster":
            self.monster_index = (self.monster_index + 1) % len(self.monsters)

    def confirm_selection(self):
        if self.selection_mode == "action":
            if self.available_actions[self.action_index] == "Attack":
                if self.monsters:  # Only switch to monster selection if there are monsters
                    self.selection_mode = "monster"
                    self.monster_index = 0
                else:
                    self.set_combat_message("No monsters to attack!")
            elif self.available_actions[self.action_index] == "Use Item":
                self.set_combat_message("Item use not implemented yet.")
            elif self.available_actions[self.action_index] == "Flee":
                self.attempt_flee()
        elif self.selection_mode == "monster" and self.monsters:
            self.selected_monster = self.monsters[self.monster_index]
            self.player_attack()

    def attempt_flee(self):
        # Simple flee mechanic: 50% chance to successfully flee
        if random.random() < 0.5:
            self.end_combat("You successfully fled from combat!")
        else:
            self.set_combat_message("Failed to flee. You lose your turn!")
            self.next_turn()
