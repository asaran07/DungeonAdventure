from typing import List

from src.characters.dungeon_character import DungeonCharacter
from src.characters.monster import Monster
from src.characters.player import Player
from src.enums.combat_state import CombatState
from src.enums.game_state import GameState
from src.exceptions import GameStateError, InvalidPlayerActionError
from src.exceptions.combat import CombatError, CharacterNotInCombatError, InvalidCombatStateError
from src.game.dungeon_adventure import GameModel
from src.views.view import View


class CombatHandler:
    def __init__(self, game_model: GameModel, view: View):
        self.game_model = game_model
        self.view = view
        self.player: Player = game_model.player
        self.monsters: List[Monster] = []
        self.turn_order: List[DungeonCharacter] = []
        self.combat_state: CombatState = CombatState.WAITING

    def initiate_combat(self):
        print(self.player.current_room.monsters)
        self.monsters = self.player.current_room.monsters
        if not self.monsters:
            raise CombatError("Cannot initiate combat without monsters")
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
        if not isinstance(character, DungeonCharacter):
            raise CharacterNotInCombatError(f"{character} is not a valid combat entity")

        if index >= len(self.turn_order):
            self.turn_order.append(character)
        elif character.attack_speed > self.turn_order[index].attack_speed:
            self.turn_order.insert(index, character)
        else:
            self._insert_into_turn_order(character, index + 1)

    def add_character(self, character: DungeonCharacter):
        if not isinstance(character, DungeonCharacter):
            raise CharacterNotInCombatError(f"{character} is not a valid combat entity")
        self._insert_into_turn_order(character)

    def start_combat(self):
        while self.game_model.game_state == GameState.IN_COMBAT:
            try:
                if self.combat_state == CombatState.PLAYER_TURN:
                    self.player_turn()
                elif self.combat_state == CombatState.MONSTER_TURN:
                    self.monster_turn()
                else:
                    raise InvalidCombatStateError(f"Invalid combat state: {self.combat_state}")
            except GameStateError as e:
                self.view.display_message(f"Game State Error: {e}")
                self.reset_combat()
            except InvalidPlayerActionError as e:
                self.view.display_message(f"Invalid Player Action: {e}")
                # TODO: Let the player retry their exception here
            except CombatError as e:
                self.view.display_message(f"Combat Error: {e}")
                self.reset_combat()
            except Exception as e:
                self.view.display_message(f"An unexpected error occurred: {e}")
                self.reset_combat()

    def player_turn(self):
        if self.game_model.game_state != GameState.IN_COMBAT:
            raise GameStateError("Player turn attempted outside of combat")
        # Logic for player turn, e.g. attack, use item, flee
        print(str(self.player.hero))
        print("\nPeople: ")
        print(self.turn_order)

    def monster_turn(self):
        if self.game_model.game_state != GameState.IN_COMBAT:
            raise GameStateError("Monster turn attempted outside of combat")
        # Logic for monster's turn
        pass

    def reset_combat(self):
        self.combat_state = CombatState.WAITING
        self.game_model.game_state = GameState.EXPLORING
        self.monsters = []
        self.turn_order = []
        self.view.display_message("Combat has been reset due to an error.")
