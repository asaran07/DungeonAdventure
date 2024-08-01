import random
from typing import Dict


# TODO: Make this class ABSTRACT lmao
class DungeonCharacter:
    def __init__(
        self,
        name: str = "Generic Character",
        max_hp: int = 20,
        base_min_damage: int = 1,
        base_max_damage: int = 5,
        attack_speed: int = 5,
        base_hit_chance: int = 70,
    ):
        """
        Initialize a DungeonCharacter.
        :param name: Character's name
        :param max_hp: Maximum hit points
        :param base_min_damage: Minimum base damage
        :param base_max_damage: Maximum base damage
        :param attack_speed: Speed of attacks
        :param base_hit_chance: Base chance to hit (percentage)
        """
        self._name: str = name
        self._max_hp: int = max_hp
        self._current_hp: int = max_hp
        self._base_min_damage: int = base_min_damage
        self._base_max_damage: int = base_max_damage
        self._attack_speed: int = attack_speed
        self._base_hit_chance: int = base_hit_chance
        self._stat_modifiers: Dict[str, int] = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value: int):
        self._current_hp = max(0, min(value, self._max_hp))

    @max_hp.setter
    def max_hp(self, value: int):
        # TODO: Add some sort of check for invalid values
        self._max_hp = value

    @property
    def base_min_damage(self) -> int:
        return self._base_min_damage

    @property
    def base_max_damage(self) -> int:
        return self._base_max_damage

    @base_max_damage.setter
    def base_max_damage(self, value: int):
        if value < self._base_min_damage:
            raise ValueError(
                "Base maximum damage cannot be less than base minimum damage"
            )
        self._base_max_damage = value

    @base_min_damage.setter
    def base_min_damage(self, value: int):
        if value < 0:
            raise ValueError("Base minimum damage cannot be negative")
        if value > self._base_max_damage:
            raise ValueError(
                "Base minimum damage cannot be greater than base maximum damage"
            )
        self._base_min_damage = value

    @property
    def attack_speed(self) -> int:
        return self._attack_speed

    @property
    def base_hit_chance(self) -> int:
        return self._base_hit_chance

    @property
    def stat_modifiers(self) -> Dict[str, int]:
        return (
            self._stat_modifiers.copy()
        )  # Return a copy to prevent direct modification

    @property
    def is_alive(self) -> bool:
        """Check if the character is still alive."""
        return self._current_hp > 0

    def attempt_attack(self, target: "DungeonCharacter") -> int:
        """
        Attempt to attack a target.
        :param target: The character to attack
        :return: Damage dealt (0 if missed)
        """
        if not self.is_alive:
            return 0
        if self._attack_hits():
            damage = self._calculate_damage()
            target.take_damage(damage)
            return damage
        return 0

    def _attack_hits(self) -> bool:
        """Determine if an attack hits based on hit chance."""
        return random.randint(1, 100) <= self.get_total_hit_chance()

    def _calculate_damage(self) -> int:
        """Calculate the damage for a successful attack."""
        min_damage = self._base_min_damage + self._stat_modifiers.get("min_damage", 0)
        max_damage = self._base_max_damage + self._stat_modifiers.get("max_damage", 0)
        return random.randint(min_damage, max_damage)

    def get_total_hit_chance(self) -> int:
        """Calculate total hit chance including modifiers."""
        return self._base_hit_chance + self._stat_modifiers.get("hit_chance", 0)

    def take_damage(self, damage: int) -> None:
        """
        Apply damage to the character.
        :param damage: Amount of damage to take
        """
        mitigated_damage = self._mitigate_damage(damage)
        self.current_hp -= mitigated_damage

    def _mitigate_damage(self, damage: int) -> int:
        """
        Calculate mitigated damage. Can be overridden by subclasses.
        :param damage: Original damage
        :return: Mitigated damage
        """
        return damage

    def heal(self, amount: int) -> None:
        """
        Heal the character.
        :param amount: Amount of hit points to restore
        """
        self.current_hp += amount

    def reset_health(self) -> None:
        """Reset health to maximum."""
        self.current_hp = self._max_hp

    def add_stat_modifier(self, stat: str, value: int) -> None:
        """
        Add a modifier to a stat.
        :param stat: Stat to modify (e.g., 'min_damage', 'hit_chance')
        :param value: Value to add to the stat
        """
        self._stat_modifiers[stat] = self._stat_modifiers.get(stat, 0) + value

    def remove_stat_modifier(self, stat: str) -> None:
        """
        Remove a stat modifier.
        :param stat: Stat to remove modifier from
        """
        self._stat_modifiers.pop(stat, None)

    def simulate_attack_roll(self) -> tuple[int, bool]:
        """
        Simulate a D20 roll for attack visualization.
        :return: Tuple of (roll result, whether the attack would hit)
        """
        roll = random.randint(1, 20)
        would_hit = roll >= (20 * (1 - self.get_total_hit_chance() / 100))
        return roll, would_hit
