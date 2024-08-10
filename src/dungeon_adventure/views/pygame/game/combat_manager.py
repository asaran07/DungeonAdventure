from typing import List
import pygame
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

    def initiate_combat(self):
        self.monsters = self.game_world.current_room.room.monsters
        if not self.monsters:
            return

        self.game_world.game_model.game_state = GameState.IN_COMBAT
        self.determine_turn_order()
        self.combat_state = CombatState.PLAYER_TURN
        self.current_turn = 0

    def determine_turn_order(self):
        self.turn_order = [self.player.hero] + self.monsters
        self.turn_order.sort(key=lambda x: x.attack_speed, reverse=True)

    def update(self):
        if self.game_world.game_model.game_state != GameState.IN_COMBAT:
            return

        current_character = self.turn_order[self.current_turn]

        if isinstance(current_character, Monster):
            self.handle_monster_turn(current_character)
        else:
            self.handle_player_turn()

    def handle_player_turn(self):
        pass

    def handle_monster_turn(self, monster: Monster):
        damage = monster.attempt_attack(self.player.hero)
        print(f"{monster.name} deals {damage} damage to you!")
        self.next_turn()

    def player_attack(self, target: Monster):
        damage = self.player.hero.attempt_attack(target)
        print(f"You deal {damage} damage to {target.name}!")
        self.check_combat_end(target)
        self.next_turn()

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        if self.current_turn == 0:
            self.combat_state = CombatState.PLAYER_TURN
        else:
            self.combat_state = CombatState.MONSTER_TURN

    def check_combat_end(self, target: Monster):
        if not target.is_alive:
            self.monsters.remove(target)
            self.turn_order.remove(target)
            self.player.hero.gain_xp(target.xp_reward)
            print(f"{target.name} has been defeated! You gained {target.xp_reward} XP.")

        if not self.monsters:
            self.end_combat("All monsters defeated!")
        elif not self.player.hero.is_alive:
            self.end_combat("Player has been defeated!")
            self.game_world.game_model.set_game_over(True)

    def end_combat(self, message: str):
        print(message)
        self.game_world.game_model.game_state = GameState.EXPLORING
        self.combat_state = CombatState.WAITING
        self.monsters = []
        self.turn_order = []

    def draw(self, surface: pygame.Surface):
        pass

    def handle_event(self, event: pygame.event.Event):
        pass
