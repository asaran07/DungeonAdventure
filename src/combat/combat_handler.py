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
        # Find turn order based on speeds
        pass

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
