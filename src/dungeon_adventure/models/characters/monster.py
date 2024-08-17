import logging
import random
import sqlite3
from typing import List, Optional

from dungeon_adventure.models.characters.dungeon_character import DungeonCharacter
from dungeon_adventure.models.items import Item


class Monster(DungeonCharacter):
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
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initialize_database()
        # self.insert_sample_data()

    def take_damage(self, damage: int) -> None:
        """
        Apply damage to the monster and attempt to heal.

        :param damage: Amount of damage to take
        """
        super().take_damage(damage)
        self.attempt_heal()

    def generate_random_monster(self):
        monster_types = ["Skeleton", "Gremlin", "Ogre"]
        monster_name = random.choice(monster_types)
        print(f"Attempting to generate a {monster_name}")

        monster_data = self.get_SQL_monster_info(monster_name)
        print(f"Data returned from get_SQL_monster_info: {monster_data}")
        print(f"Type of monster_data: {type(monster_data)}")

        if monster_data and isinstance(monster_data, tuple):
            try:
                return Monster(
                    name=str(monster_data[1]),
                    max_hp=int(monster_data[2]),
                    base_min_damage=int(monster_data[3]),
                    base_max_damage=int(monster_data[4]),
                    attack_speed=int(monster_data[5]),
                    base_hit_chance=int(monster_data[6]),
                    heal_chance=int(monster_data[7]),
                    min_heal=int(monster_data[8]),
                    max_heal=int(monster_data[9]),
                    xp_reward=int(monster_data[10]),
                )
            except Exception as e:
                print(f"Error creating monster from data: {e}")
                print(f"monster_data: {monster_data}")
        else:
            print(f"Invalid data returned for monster: {monster_name}")

        # Fallback to default monster creation
        return Monster(name=monster_name)

    def attempt_heal(self) -> int:
        """
        Attempt to heal based on healed chance.

        :return: Amount healed (0 if healing didn't occur)
        """
        if random.randint(1, 100) <= self.heal_chance:
            self.logger.info(
                f"Monster heal chance successful, healing for {self.heal_chance}"
            )
            heal_amount = random.randint(self.min_heal, self.max_heal)
            self.heal(heal_amount)
            return heal_amount
        self.logger.info(f"Healing failed for {self.name}")
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

    def initialize_database(self):
        try:
            with sqlite3.connect("monster_factory_new.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS monster_factory_new (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        max_hp INTEGER,
                        base_min_damage INTEGER,
                        base_max_damage INTEGER,
                        attack_speed INTEGER,
                        base_hit_chance INTEGER,
                        heal_chance INTEGER,
                        min_heal INTEGER,
                        max_heal INTEGER,
                        xp_reward INTEGER
                    )
                """
                )
                conn.commit()
            print("Database initialized successfully")
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")

    def insert_sample_data(self):
        try:
            with sqlite3.connect("monster_factory_new.db") as conn:
                cursor = conn.cursor()

                # Check if the table is empty
                cursor.execute("SELECT COUNT(*) FROM monster_factory_new")
                count = cursor.fetchone()[0]

                if count == 0:
                    cursor.executemany(
                        """
                        INSERT INTO monster_factory_new 
                        (name, max_hp, base_min_damage, base_max_damage, attack_speed, base_hit_chance, heal_chance, min_heal, max_heal, xp_reward)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        [
                            ("Skeleton", 100, 10, 20, 5, 70, 10, 5, 10, 50),
                            ("Gremlin", 70, 15, 30, 5, 80, 20, 10, 20, 100),
                            ("Ogre", 200, 30, 50, 3, 60, 10, 30, 50, 200),
                        ],
                    )
                    conn.commit()
                    print("Sample data inserted successfully")
                else:
                    print("Table already contains data, skipping insertion")
        except sqlite3.Error as e:
            print(f"Error inserting sample data: {e}")

    def get_SQL_monster_info(self, name: str) -> Optional[tuple]:
        try:
            with sqlite3.connect("monster_factory_new.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM monster_factory_new WHERE name = ? LIMIT 1", (name,)
                )
                record = cursor.fetchone()
                if not record:
                    print(f"No data found for monster: {name}")
                return record
        except sqlite3.Error as e:
            print(f"Database error: {e}")
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


def test_db_connection():
    monster = Monster()
    monster.initialize_database()
    monster.insert_sample_data()

    monster_types = ["Skeleton", "Gremlin", "Ogre"]
    for monster_type in monster_types:
        result = monster.get_SQL_monster_info(monster_type)
        print(f"Test query result for {monster_type}: {result}")


if __name__ == "__main__":
    test_db_connection()
