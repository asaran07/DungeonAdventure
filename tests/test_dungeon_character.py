import unittest
from dungeon_adventure.models.characters.dungeon_character import DungeonCharacter


class TestDungeonCharacter(unittest.TestCase):

    def setUp(self):
        self.character = DungeonCharacter("Test Character", 100, 10, 20, 5, 80)

    def test_initialization(self):
        self.assertEqual(self.character.name, "Test Character")
        self.assertEqual(self.character.max_hp, 100)
        self.assertEqual(self.character.current_hp, 100)
        self.assertEqual(self.character.base_min_damage, 10)
        self.assertEqual(self.character.base_max_damage, 20)
        self.assertEqual(self.character.attack_speed, 5)
        self.assertEqual(self.character.base_hit_chance, 80)

    def test_name_setter(self):
        self.character.name = "New Name"
        self.assertEqual(self.character.name, "New Name")
        with self.assertRaises(ValueError):
            self.character.name = ""

    def test_current_hp_setter(self):
        self.character.current_hp = 50
        self.assertEqual(self.character.current_hp, 50)
        self.character.current_hp = 150
        self.assertEqual(self.character.current_hp, 100)
        self.character.current_hp = -10
        self.assertEqual(self.character.current_hp, 0)

    def test_base_damage_setters(self):
        self.character.base_min_damage = 15
        self.assertEqual(self.character.base_min_damage, 15)
        with self.assertRaises(ValueError):
            self.character.base_min_damage = 25
        with self.assertRaises(ValueError):
            self.character.base_min_damage = -5

        self.character.base_max_damage = 30
        self.assertEqual(self.character.base_max_damage, 30)
        with self.assertRaises(ValueError):
            self.character.base_max_damage = 10

    def test_is_alive(self):
        self.assertTrue(self.character.is_alive)
        self.character.current_hp = 0
        self.assertFalse(self.character.is_alive)

    def test_take_damage(self):
        self.character.take_damage(30)
        self.assertEqual(self.character.current_hp, 70)

    def test_heal(self):
        self.character.current_hp = 50
        self.character.heal(30)
        self.assertEqual(self.character.current_hp, 80)
        self.character.heal(30)
        self.assertEqual(self.character.current_hp, 100)

    def test_reset_health(self):
        self.character.current_hp = 50
        self.character.reset_health()
        self.assertEqual(self.character.current_hp, 100)

    def test_stat_modifiers(self):
        self.character.add_stat_modifier("min_damage", 5)
        self.assertEqual(self.character.stat_modifiers["min_damage"], 5)
        self.character.add_stat_modifier("min_damage", 3)
        self.assertEqual(self.character.stat_modifiers["min_damage"], 8)
        self.character.remove_stat_modifier("min_damage")
        self.assertNotIn("min_damage", self.character.stat_modifiers)

    def test_get_total_hit_chance(self):
        self.assertEqual(self.character.get_total_hit_chance(), 80)
        self.character.add_stat_modifier("hit_chance", 10)
        self.assertEqual(self.character.get_total_hit_chance(), 90)

    def test_simulate_attack_roll(self):
        roll, would_hit = self.character.simulate_attack_roll()
        self.assertTrue(1 <= roll <= 20)
        self.assertIsInstance(would_hit, bool)

    def test_attempt_attack(self):
        target = DungeonCharacter("Target", 100, 1, 1, 1, 1)
        damage = self.character.attempt_attack(target)
        self.assertTrue(0 <= damage <= 20)
        self.assertTrue(80 <= target.current_hp <= 100)


if __name__ == '__main__':
    unittest.main()
