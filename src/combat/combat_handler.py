from typing import List

from src.characters.dungeon_character import DungeonCharacter
from src.characters.monster import Monster
from src.characters.player import Player
from src.enums.combat_state import CombatState
from src.enums.game_state import GameState
from src.exceptions import GameStateError, InvalidPlayerActionError
from src.exceptions.combat import (
    CombatError,
    CharacterNotInCombatError,
    InvalidCombatStateError,
)
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
        self.monsters = self.player.current_room.monsters
        if not self.monsters:
            raise CombatError("Cannot initiate combat without monsters")
        self.game_model.game_state = GameState.IN_COMBAT
        self.determine_turn_order()
        self.combat_state = CombatState.PLAYER_TURN  # Start with player's turn
        self.start_combat()

    def determine_turn_order(self):
        self.turn_order = []
        all_characters = self.monsters + [self.player.hero]
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

    # TODO: Make this method smaller by extraction into helper methods with descriptive names
    def start_combat(self):
        while self.game_model.game_state == GameState.IN_COMBAT:
            try:
                self.view.display_combat_status(self.player, self.monsters)
                if self.combat_state == CombatState.PLAYER_TURN:
                    self.player_turn()
                elif self.combat_state == CombatState.MONSTER_TURN:
                    self.monster_turn()
                else:
                    raise InvalidCombatStateError(
                        f"Invalid combat state: {self.combat_state}"
                    )
            except GameStateError as e:
                self.view.display_message(f"Game State Error: {e}")
                self.reset_combat()
            except InvalidPlayerActionError as e:
                self.view.display_message(f"Invalid Player Action: {e}")
                continue
            except CombatError as e:
                self.view.display_message(f"Combat Error: {e}")
                self.reset_combat()
            except Exception as e:
                self.view.display_message(f"An unexpected error occurred: {e}")
                self.reset_combat()

    def check_combat_end(self, target: Monster):
        # Remove dead monsters
        # self.monsters = [monster for monster in self.monsters if monster.is_alive]

        if not target.is_alive:
            self.view.display_message(f"{target.name} has been defeated!")
        if not self.monsters:
            self.end_combat("All monsters defeated!")
        elif not self.player.hero.is_alive:
            self.end_combat("Player has been defeated!")
        self.combat_state = CombatState.MONSTER_TURN

    def end_combat(self, message):
        self.view.display_message(message)
        self.game_model.game_state = GameState.EXPLORING
        self.reset_combat()

    def player_turn(self):
        if self.game_model.game_state != GameState.IN_COMBAT:
            raise GameStateError("Player turn attempted outside of combat")
        action = self.view.get_combat_action()
        if action == "attack":
            self.player_attack()
        elif action == "use_item":
            # Implement item use logic
            pass
        elif action == "flee":
            # Implement flee logic
            pass
        else:
            raise InvalidPlayerActionError(f"Invalid action: {action}")
        # self.combat_state = CombatState.MONSTER_TURN

    def player_attack(self):
        # TODO: Clean up this method
        target: Monster = self.view.get_combat_target(self.monsters)
        self.is_valid_target(target)
        damage = self.player.hero.attempt_attack(target)
        self.view.display_message(f"You deal {damage} damage to {target.name}!")
        self.check_combat_end(target)

    def is_valid_target(self, target: Monster):
        if target is None:
            raise InvalidPlayerActionError("Invalid target")

    def handle_xp_gain(self, xp_amount: int):
        self.player.hero.gain_xp(xp_amount)
        self.view.display_xp_gained(xp_amount)

    def monster_turn(self):
        for monster in self.monsters:
            if monster.is_alive:
                damage = monster.attempt_attack(self.player.hero)
                self.view.display_message(
                    f"{monster.name} deals {damage} damage to you!"
                )
                if not self.player.hero.is_alive:
                    return  # End the monster turn if the player is defeated
        self.combat_state = CombatState.PLAYER_TURN

    def reset_combat(self):
        self.combat_state = CombatState.WAITING
        self.game_model.game_state = GameState.EXPLORING
        self.monsters = []
        self.turn_order = []
        self.view.display_message("Combat has been reset.")
