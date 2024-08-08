import random
import sqlite3
from typing import List, Optional

from dungeon_adventure.models.characters.dungeon_character import DungeonCharacter
from dungeon_adventure.models.items import Item


class Monster(DungeonCharacter):
    # TODO: Add properties for get and set
    def __init__(
        self,
        name: str = "Generic Monster",
        max_hp: int = 20,
        base_min_damage: int = 1,
        base_max_damage: int = 5,
        attack_speed: int = 5,
        base_hit_chance: int = 70,
        heal_chance: int = 10,
        min_heal: int = 5,
        max_heal: int = 10,
        xp_reward: int = 50,
        loot: Optional[List[Item]] = None,
    ):
        super().__init__(
            name,
            max_hp,
            base_min_damage,
            base_max_damage,
            attack_speed,
            base_hit_chance,
        )
        self.heal_chance: int = heal_chance
        self.min_heal: int = min_heal
        self.max_heal: int = max_heal
        self.xp_reward: int = xp_reward
        self.loot: List[Item] = loot if loot is not None else []

    def attempt_heal(self) -> int:
        """
        Attempt to heal based on heal chance.

        :return: Amount healed (0 if healing didn't occur)
        """
        if random.randint(1, 100) <= self.heal_chance:
            heal_amount = random.randint(self.min_heal, self.max_heal)
            self.heal(heal_amount)
            return heal_amount
        return 0

    def drop_loot(self) -> List[Item]:
        """
        Return the monster's loot when defeated.

        :return: List of Item objects
        """
        dropped_loot = self.loot.copy()
        self.loot.clear()
        return dropped_loot

    def attempt_attack(self, target: DungeonCharacter) -> int:
        """
        Attempt to attack and then try to heal.

        :param target: The character to attack
        :return: Damage dealt
        """
        damage_dealt = super().attempt_attack(target)
        self.attempt_heal()
        return damage_dealt

    @classmethod
    def create_custom_monster(cls, **kwargs):
        """
        Create a custom monster with specified attributes.

        :param kwargs: Key-value pairs of attributes to customize
        :return: A new Monster instance with custom attributes
        """
        return cls(**kwargs)


