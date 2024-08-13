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

    # def monster_type(self, name: str):
    #     data = self.get_SQL_monster_info(name)
    #     return data

    def generate_random_monster(self):
        monster_roll = random.randint(1, 3)
        monster_name = ""
        if monster_roll == 1:
            monster_name = "Skeleton"
        elif monster_roll == 2:
            monster_name = "Gremlin"
        else:
            monster_name = "Ogre"

        print(f"Attempting to generate a {monster_name}")

        data = self.get_SQL_monster_info(monster_name)
        print(f"Data returned from get_SQL_monster_info: {data}")

        if data is not None and len(data) > 0:
            monster_data = data[0]
            print(f"Monster data: {monster_data}")
            # Create and return Monster instance as before
            return Monster(
                name=monster_data[1],
                max_hp=monster_data[2],
                base_min_damage=monster_data[3],
                base_max_damage=monster_data[4],
                attack_speed=monster_data[5],
                base_hit_chance=monster_data[6],
                heal_chance=monster_data[7],
                min_heal=monster_data[8],
                max_heal=monster_data[9],
                xp_reward=monster_data[10],
            )
        else:
            print(f"No data found for monster: {monster_name}")
            return Monster(name=monster_name)

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

    # def get_SQL_monster_info(self, name: str) -> List[any]:
    #     try:
    #         sqliteConnection = sqlite3.connect("monster_factory_new.db")
    #         cursor = sqliteConnection.cursor()
    #         print("Connected to SQLite")
    #
    #         sqlite_select_query = """select * from monster_factory_new where name = ?"""
    #         cursor.execute(sqlite_select_query, (name,))
    #         records = cursor.fetchall()
    #         cursor.close()
    #         return records
    #
    #     except sqlite3.Error as error:
    #         print("Failed to read data from sqlite", error)
    #     finally:
    #         if sqliteConnection:
    #             sqliteConnection.close()
    #             print("SQLite connection is closed")

    def get_SQL_monster_info(self, name: str) -> List[any]:
        try:
            with sqlite3.connect("monster_factory_new.db") as sqliteConnection:
                cursor = sqliteConnection.cursor()
                print("Connected to SQLite")

                sqlite_select_query = (
                    """select * from monster_factory_new where name = ?"""
                )
                cursor.execute(sqlite_select_query, (name,))
                records = cursor.fetchall()
                return records if records else None

        except sqlite3.Error as error:
            print("Failed to read data from sqlite", error)
            return None

    def __str__(self):
        """
        Get a string representation of Monster Name

        :return: A string representation of Monster's name
        """
        return f"{self.name}"

    def __repr__(self):
        """
        Get a string representation of Monster name from a list

        :return: A string representation of Monster name from a list:
        """
        return self.__str__()
