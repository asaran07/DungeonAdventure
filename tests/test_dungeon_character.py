import unittest
from unittest.mock import patch
from src.characters.dungeon_character import DungeonCharacter


class TestDungeonCharacter(unittest.TestCase):

    def setUp(self):
        self.character = DungeonCharacter("Test Character", 100, 5,
                                          10, 5, 70)

    def test_init(self):
        self.assertEqual(self.character.name, "Test Character")
        self.assertEqual(self.character.max_hp, 100)
        self.assertEqual(self.character.current_hp, 100)
        self.assertEqual(self.character.base_min_damage, 5)
        self.assertEqual(self.character.base_max_damage, 10)
        self.assertEqual(self.character.attack_speed, 5)
        self.assertEqual(self.character.base_hit_chance, 70)
        self.assertEqual(self.character.stat_modifiers, {})

    @patch('random.randint')
    def test_simulate_attack_roll(self, mock_randint):
        mock_randint.return_value = 15
        roll, would_hit = self.character.simulate_attack_roll()
        self.assertEqual(roll, 15)
        self.assertTrue(would_hit)

        mock_randint.return_value = 5
        roll, would_hit = self.character.simulate_attack_roll()
        self.assertEqual(roll, 5)
        self.assertFalse(would_hit)

    @patch('random.randint')
    def test_attack_hit(self, mock_randint):
        mock_randint.side_effect = [50, 7]  # First for hit chance, second for damage
        target = DungeonCharacter("Target", 100, 1, 5, 5, 70)
        damage = self.character.attempt_attack(target)
        self.assertEqual(damage, 7)
        self.assertEqual(target.current_hp, 93)

    @patch('random.randint')
    def test_attack_miss(self, mock_randint):
        mock_randint.return_value = 80  # Above hit chance, so it should miss
        target = DungeonCharacter("Target", 100, 1, 5, 5, 70)
        damage = self.character.attempt_attack(target)
        self.assertEqual(damage, 0)
        self.assertEqual(target.current_hp, 100)

    def test_attack_when_ko(self):
        # Set the character's HP to 0
        self.character.current_hp = 0

        # Create a target
        target = DungeonCharacter("Target", 100, 5, 10, 5, 70)
        initial_target_hp = target.current_hp

        # Ensure the character is not alive
        self.assertFalse(self.character.is_alive)

        # Attempt to attack
        damage = self.character.attempt_attack(target)

        # Check that no damage was dealt
        self.assertEqual(damage, 0)

        # Verify that the target's HP didn't change
        self.assertEqual(target.current_hp, initial_target_hp)

        # Double-check that the character is still not alive
        self.assertFalse(self.character.is_alive)

    @patch('random.randint')
    def test_lose_health(self, mock_randint):
        mock_randint.return_value = 8

        attacker = DungeonCharacter("Attacker", 100, 5, 10, 5, 70)
        damage = attacker.attempt_attack(self.character)

        self.assertEqual(damage, 8)
        self.assertEqual(self.character.current_hp, 92)

        # Test with a different damage roll
        mock_randint.return_value = 6
        damage = attacker.attempt_attack(self.character)

        self.assertEqual(damage, 6)
        self.assertEqual(self.character.current_hp, 86)

    @patch('random.randint')
    def test_lose_health_ko(self, mock_randint):
        self.character.current_hp = 0

        # Ensure the character is not alive
        self.assertFalse(self.character.is_alive)

        # Attempt to deal damage
        self.character.take_damage(20)

        # Check that HP remains at 0 and doesn't go negative
        self.assertEqual(self.character.current_hp, 0)

        # Double-check that the character is still not alive
        self.assertFalse(self.character.is_alive)

    def test_is_alive(self):
        self.assertTrue(self.character.is_alive)
        self.character.current_hp = 0
        self.assertFalse(self.character.is_alive)

    def test_heal(self):
        self.character.current_hp = 50
        self.character.heal(30)
        self.assertEqual(self.character.current_hp, 80)
        self.character.heal(30)
        self.assertEqual(self.character.current_hp, 100)  # Should not exceed max_hp

    def test_reset_health(self):
        self.character.current_hp = 50
        self.character.reset_health()
        self.assertEqual(self.character.current_hp, 100)

    def test_add_remove_stat_modifier(self):
        self.character.add_stat_modifier('min_damage', 2)
        self.assertEqual(self.character.stat_modifiers['min_damage'], 2)
        self.character.add_stat_modifier('min_damage', 3)
        self.assertEqual(self.character.stat_modifiers['min_damage'], 5)
        self.character.remove_stat_modifier('min_damage')
        self.assertNotIn('min_damage', self.character.stat_modifiers)


if __name__ == '__main__':
    unittest.main()
