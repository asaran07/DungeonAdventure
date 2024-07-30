from typing import Dict
import random


class DungeonCharacter:
    def __init__(self, name: str = "Generic Character",
                 max_hp: int = 100,
                 base_min_damage: int = 1,
                 base_max_damage: int = 10,
                 attack_speed: int = 5,
                 base_hit_chance: int = 70):
        """
        Initialize a DungeonCharacter.

        :param name: Character's name
        :param max_hp: Maximum hit points
        :param base_min_damage: Minimum base damage
        :param base_max_damage: Maximum base damage
        :param attack_speed: Speed of attacks
        :param base_hit_chance: Base chance to hit (percentage)
        """
        self.name: str = name
        self.max_hp: int = max_hp
        self.current_hp: int = max_hp
        self.base_min_damage: int = base_min_damage
        self.base_max_damage: int = base_max_damage
        self.attack_speed: int = attack_speed
        self.base_hit_chance: int = base_hit_chance
        self.stat_modifiers: Dict[str, int] = {}

    @property
    def is_alive(self) -> bool:
        """Check if the character is still alive."""
        return self.current_hp > 0

    def attempt_attack(self, target: 'DungeonCharacter') -> int:
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
        min_damage = self.base_min_damage + self.stat_modifiers.get('min_damage', 0)
        max_damage = self.base_max_damage + self.stat_modifiers.get('max_damage', 0)
        return random.randint(min_damage, max_damage)

    def get_total_hit_chance(self) -> int:
        """Calculate total hit chance including modifiers."""
        return self.base_hit_chance + self.stat_modifiers.get('hit_chance', 0)

    def take_damage(self, damage: int) -> None:
        """
        Apply damage to the character.

        :param damage: Amount of damage to take
        """
        mitigated_damage = self._mitigate_damage(damage)
        self.current_hp = max(0, self.current_hp - mitigated_damage)

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
        self.current_hp = min(self.max_hp, self.current_hp + amount)

    def reset_health(self) -> None:
        """Reset health to maximum."""
        self.current_hp = self.max_hp

    def add_stat_modifier(self, stat: str, value: int) -> None:
        """
        Add a modifier to a stat.

        :param stat: Stat to modify (e.g., 'min_damage', 'hit_chance')
        :param value: Value to add to the stat
        """
        self.stat_modifiers[stat] = self.stat_modifiers.get(stat, 0) + value

    def remove_stat_modifier(self, stat: str) -> None:
        """
        Remove a stat modifier.

        :param stat: Stat to remove modifier from
        """
        self.stat_modifiers.pop(stat, None)

    def simulate_attack_roll(self) -> tuple[int, bool]:
        """
        Simulate a D20 roll for attack visualization.

        :return: Tuple of (roll result, whether the attack would hit)
        """
        roll = random.randint(1, 20)
        would_hit = roll >= (20 * (1 - self.get_total_hit_chance() / 100))
        return roll, would_hit
