import random
import sqlite3
from typing import Optional, List

from dungeon_adventure.models.characters.dungeon_character import DungeonCharacter
from dungeon_adventure.models.items import Weapon


class Hero(DungeonCharacter):
    def __init__(
        self,
        name: str = "Hero",
        max_hp: int = 75,
        base_min_damage: int = 10,
        base_max_damage: int = 20,
        attack_speed: int = 5,
        base_hit_chance: int = 70,
        block_chance: int = 20,
    ):
        super().__init__(
            name,
            max_hp,
            base_min_damage,
            base_max_damage,
            attack_speed,
            base_hit_chance,
        )
        self.current_hp = max_hp
        self.block_chance: int = block_chance
        self.level: int = 1
        self.xp: int = 0
        self.xp_to_next_level: int = 100  # Starting XP required for level 2
        self.equipped_weapon: Optional[Weapon] = None

    def hero_class(self, name: str):
        data = self.get_SQL_hero_info(name)
        for item in data:
            print(item)

    def _mitigate_damage(self, damage: int) -> int:
        """Attempt to block incoming damage."""
        if random.randint(1, 100) <= self.block_chance:
            blocked_damage = int(damage * 0.5)  # Block 50% of incoming damage
            return damage - blocked_damage
        return damage

    def equip_weapon(self, weapon: Weapon) -> None:
        """Equip a weapon and apply its stat modifiers."""
        if self.equipped_weapon:
            self._remove_weapon_modifiers()

        self.equipped_weapon = weapon
        self._apply_weapon_modifiers(weapon)

    def _apply_weapon_modifiers(self, weapon: Weapon) -> None:
        """Apply weapon stat modifiers."""
        self.add_stat_modifier("min_damage", weapon.min_damage)
        self.add_stat_modifier("max_damage", weapon.max_damage)
        # Add other weapon stat modifiers as needed

    def _remove_weapon_modifiers(self) -> None:
        """Remove weapon stat modifiers."""
        self.remove_stat_modifier("min_damage")
        self.remove_stat_modifier("max_damage")

    def gain_xp(self, xp: int) -> None:
        """Gain experience points and level up if necessary."""
        self.xp += xp
        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self) -> None:
        """Increase level and update stats."""
        self.level += 1
        self.max_hp += 10
        self.current_hp = self.max_hp
        self.base_min_damage += 2
        self.base_max_damage += 2
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = self._calculate_next_level_xp()

    def _calculate_next_level_xp(self) -> int:
        """Calculate XP required for the next level using a Fibonacci-like sequence."""
        return int(self.xp_to_next_level * 1.5)

    def attempt_attack(self, target: "DungeonCharacter") -> int:
        """Override to add any hero-specific attack logic."""
        return super().attempt_attack(target)

    # Placeholder for future special ability implementation
    def use_special_ability(self) -> None:
        """Use a special ability. To be implemented by subclasses."""
        # if name == warrior/do warrior Crushing Blow etc.
        pass

    def __str__(self) -> str:
        weapon_info = (
            f"Equipped: {self.equipped_weapon.name}"
            if self.equipped_weapon
            else "No weapon equipped"
        )
        return (
            f"Hero: {self.name}\n"
            f"Level: {self.level}\n"
            f"HP: {self.current_hp}/{self.max_hp}\n"
            f"XP: {self.xp}/{self.xp_to_next_level}\n"
            f"Damage: {self.base_min_damage}-{self.base_max_damage}\n"
            f"Hit Chance: {self.base_hit_chance}%\n"
            f"Block Chance: {self.block_chance}%\n"
            f"{weapon_info}"
        )

    def get_SQL_hero_info(self, name:str) -> List[any]:
        try:
            sqliteConnection = sqlite3.connect("hero_factory.db")
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """select * from hero_factory where name = ?"""
            cursor.execute(sqlite_select_query, (name,))
            records = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("SQLite connection is closed")

        return records

# if __name__ == "__main__":
#     hero = Hero()
#     hero.hero_class("Thief")
