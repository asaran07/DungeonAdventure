from typing import List, Optional

from src.characters.dungeon_character import DungeonCharacter
from src.characters.monster import Monster
from src.characters.player import Player
from src.enums.combat_state import CombatState
from src.enums.game_state import GameState
from src.views.view import View


class CombatHandler:
    def __init__(self, game_model, view: View):
        self.game_model = game_model
        self.view = view
        self.player: Player = game_model.player
        self.monsters: List[Monster] = []
        self.turn_order: List[DungeonCharacter] = []
        self.combat_state: CombatState = CombatState.WAITING

    def initiate_combat(self, monsters: List[Monster]):
        self.monsters = monsters
        self.game_model.game_state = GameState.IN_COMBAT
        self.determine_turn_order()
        self.combat_state = CombatState.WAITING
        self.start_combat()

    def determine_turn_order(self):
        self.turn_order = []
        all_characters = self.monsters + [self.player]

        for character in all_characters:
            self._insert_into_turn_order(character)

    def _insert_into_turn_order(self, character, index: int = 0):
        if index >= len(self.turn_order):
            self.turn_order.append(character)
        elif character.attack_speed > self.turn_order[index].attack_speed:
            self.turn_order.insert(index, character)
        else:
            self._insert_into_turn_order(character, index + 1)

    def add_character(self, character: DungeonCharacter):
        self._insert_into_turn_order(character)

    def start_combat(self):
        while self.game_model.game_state == GameState.IN_COMBAT:
            if self.combat_state == CombatState.PLAYER_TURN:
                self.player_turn()
            elif self.combat_state == CombatState.MONSTER_TURN:
                self.monster_turn()
            else:
                raise ValueError(f"Invalid combat state: {self.combat_state}")

    def player_turn(self):
        # Logic for player turn, eg. attack, use item, flee
        print(self.player)
        pass

    def monster_turn(self):
        # Logic for monster's turn
        pass
