import logging
import random
from typing import List, Optional

from dungeon_adventure.enums.combat_state import CombatState
from dungeon_adventure.enums.game_state import GameState
from dungeon_adventure.models.characters.hero import Hero
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.views.pygame.game.game_world import GameWorld


class CombatManager:
    def __init__(self, game_world: GameWorld):
        self.game_world = game_world
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
        self.logger = logging.getLogger("dungeon_adventure.combat")

    def initiate_combat(self) -> None:
        self.logger.info("Initiating combat")
        self.monsters = self.game_world.current_room.room.monsters
        if not self.monsters:
            self.logger.warning("No monsters found in current room.")
            return

        self.game_world.game_model.game_state = GameState.IN_COMBAT
        self.determine_turn_order()
        self.combat_state = CombatState.PLAYER_TURN
        self.current_turn = 0
        self.selected_monster = None

    def determine_turn_order(self) -> None:
        self.logger.info("Determining turn order")
        self.turn_order = [self.player.hero] + self.monsters
        self.turn_order.sort(key=lambda x: x.attack_speed, reverse=True)

    def handle_player_action(
        self, action: str, target_index: Optional[int] = None
    ) -> str:
        self.logger.info("Handling player action")
        if action == "Attack":
            self.logger.debug(
                "Action -> Attack, attacking monster {}".format(target_index)
            )
            if target_index is not None and 0 <= target_index < len(self.monsters):
                return self.player_attack(self.monsters[target_index])
            else:
                return "Invalid target."
        elif action == "Use Item":
            return "Item use not implemented yet."
        elif action == "Flee":
            return self.attempt_flee()
        else:
            return "Invalid action."

    def player_attack(self, target: Monster) -> str:
        damage = self.player.hero.attempt_attack(target)
        self.logger.debug("Calculated damage = {}".format(damage))
        message = f"You deal {damage} damage to {target.name}!"
        if not target.is_alive:
            self.logger.debug("Monster {} defeated".format(target.name))
            self.handle_monster_defeat(target)
        self.next_turn()
        return message

    def handle_monster_defeat(self, monster: Monster) -> None:
        self.monsters.remove(monster)
        self.turn_order.remove(monster)
        xp_gained = monster.xp_reward
        self.player.hero.gain_xp(xp_gained)
        self.total_xp_gained += xp_gained
        self.monsters_defeated += 1

    def attempt_flee(self) -> str:
        if random.random() < 0.5:
            self.end_combat()
            return "You successfully fled from combat!"
        else:
            self.next_turn()
            return "Failed to flee. You lose your turn!"

    def next_turn(self) -> None:
        self.logger.info("Advancing turn")
        if not self.turn_order:
            self.end_combat()
            return

        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        if self.current_turn == 0:
            self.logger.debug("Switching to player turn state")
            self.combat_state = CombatState.PLAYER_TURN
        else:
            self.logger.debug("Switching to monster turn state")
            self.combat_state = CombatState.MONSTER_TURN

    def handle_monster_turn(self) -> str:
        self.logger.debug("Handling turn for monster {}".format(len(self.monsters)))
        monster = self.turn_order[self.current_turn]
        damage = monster.attempt_attack(self.player.hero)
        self.next_turn()
        return f"{monster.name} deals {damage} damage to you!"

    def is_combat_over(self) -> bool:
        return not self.monsters or not self.player.hero.is_alive

    def end_combat(self) -> None:
        self.logger.debug("Ending combat")
        self.game_world.game_model.game_state = GameState.EXPLORING
        self.combat_state = CombatState.WAITING
        self.monsters = []
        self.turn_order = []
        self.total_xp_gained = 0
        self.monsters_defeated = 0
        self.combat_over = True

    def get_combat_summary(self) -> dict:
        return {
            "monsters_defeated": self.monsters_defeated,
            "total_xp_gained": self.total_xp_gained,
            "player_hp": self.player.hero.current_hp,
            "player_max_hp": self.player.hero.max_hp,
            "monsters": [
                {"name": m.name, "hp": m.current_hp, "max_hp": m.max_hp}
                for m in self.monsters
            ],
        }
