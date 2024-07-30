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
        self.display_turn_order()

    def start_combat(self):
        while self.game_model.game_state == GameState.IN_COMBAT:
            if self.combat_state == CombatState.PLAYER_TURN:
                self.player_turn()
            elif self.combat_state == CombatState.MONSTER_TURN:
                self.monster_turn()
            elif self.combat_state == CombatState.WAITING:
                self.next_turn()
            else:
                raise ValueError(f"Invalid combat state: {self.combat_state}")

    def get_next_character(self) -> DungeonCharacter:
        if not self.turn_order:
            raise ValueError("No characters in turn order")
        return self.turn_order[0]

    def display_turn_order(self):
        for character in self.turn_order:
            print(f"{character.name} (Speed: {character.attack_speed})")

    def player_turn(self):
        # Logic for player turn, eg. attack, use item, flee
        pass

    def monster_turn(self):
        # Logic for monster's turn
        pass

    def next_turn(self):
        # Logic to determine whose turn is next
        pass

    def process_attack(self, attacker: DungeonCharacter, target: DungeonCharacter):
        # Logic to handle an attack and its results
        pass

    def handle_player_flee(self):
        # Logic for when the player chooses to flee
        pass

    def check_combat_end(self):
        # Check if combat should end (all monsters defeated or player fled)
        pass

    def end_combat(self):
        # Clean up after combat ends
        self.game_model.game_state = GameState.EXPLORING
        self.combat_state = CombatState.WAITING
        # Update room's monster list if needed
        pass

    def advance_combat(self):
        # Method to wait for player input to advance combat
        pass
