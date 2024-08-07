import unittest
from unittest.mock import MagicMock, patch

from dungeon_adventure.services import ItemFactory
from src.dungeon_adventure.enums.item_types import WeaponType
from src.dungeon_adventure.models.characters import DungeonCharacter
from src.dungeon_adventure.models.characters.hero import Hero


class TestHero(unittest.TestCase):

    def setUp(self):
        self.hero = Hero("Test Hero", 100, 10, 20, 5, 70, 20)
        self.item_factory = ItemFactory()

    def test_init(self):
        self.assertEqual(self.hero.name, "Test Hero")
        self.assertEqual(self.hero.max_hp, 100)
        self.assertEqual(self.hero.current_hp, 100)
        self.assertEqual(self.hero.base_min_damage, 10)
        self.assertEqual(self.hero.base_max_damage, 20)
        self.assertEqual(self.hero.attack_speed, 5)
        self.assertEqual(self.hero.base_hit_chance, 70)
        self.assertEqual(self.hero.block_chance, 20)
        self.assertEqual(self.hero.level, 1)
        self.assertEqual(self.hero.xp, 0)
        self.assertEqual(self.hero.xp_to_next_level, 100)
        self.assertIsNone(self.hero.equipped_weapon)

    @patch("random.randint")
    def test_mitigate_damage_block(self, mock_randint):
        mock_randint.return_value = 10  # Ensure block
        mitigated = self.hero._mitigate_damage(100)
        self.assertEqual(mitigated, 50)

    @patch("random.randint")
    def test_mitigate_damage_no_block(self, mock_randint):
        mock_randint.return_value = 100  # Ensure no block
        mitigated = self.hero._mitigate_damage(100)
        self.assertEqual(mitigated, 100)

    # @unittest.skip('still need to update loot')
    def test_equip_weapon(self):
        weapon = self.item_factory.create_weapon("Sword", WeaponType.SWORD, 1, 10)
        self.hero.equip_weapon(weapon)
        self.assertEqual(self.hero.equipped_weapon, weapon)
        self.assertEqual(self.hero.stat_modifiers.get("min_damage", 1), 1)
        self.assertEqual(self.hero.stat_modifiers.get("max_damage", 3), 3)

    # @unittest.skip('still need to update loot')
    def test_equip_weapon_replace(self):
        weapon1 = self.item_factory.create_weapon("Sword", WeaponType.SWORD, 1, 10)
        weapon2 = self.item_factory.create_weapon("Bow", WeaponType.BOW, 2, 25)
        self.hero.equip_weapon(weapon1)
        self.hero.equip_weapon(weapon2)
        self.assertEqual(self.hero.equipped_weapon, weapon2)
        self.assertEqual(self.hero.stat_modifiers.get("min_damage", 1), 1)
        # bow reduces set damage by 1 for min
        self.assertEqual(self.hero.stat_modifiers.get("max_damage", 3), 3)
        # bow increases from min damage by 2 for max

    def test_gain_xp_no_level_up(self):
        self.hero.gain_xp(50)
        self.assertEqual(self.hero.xp, 50)
        self.assertEqual(self.hero.level, 1)

    def test_gain_xp_level_up(self):
        self.hero.gain_xp(150)
        self.assertEqual(self.hero.level, 2)
        self.assertEqual(self.hero.max_hp, 110)
        self.assertEqual(self.hero.current_hp, 110)
        self.assertEqual(self.hero.base_min_damage, 12)
        self.assertEqual(self.hero.base_max_damage, 22)
        self.assertEqual(self.hero.xp, 50)
        self.assertEqual(self.hero.xp_to_next_level, 150)

    def test_multiple_level_ups(self):
        self.hero.gain_xp(500)
        self.assertGreater(self.hero.level, 2)

    def test_calculate_next_level_xp(self):
        next_xp = self.hero._calculate_next_level_xp()
        self.assertEqual(next_xp, 150)

    @patch.object(DungeonCharacter, "attempt_attack")
    def test_attempt_attack(self, mock_super_attack):
        mock_super_attack.return_value = 15
        target = MagicMock(spec=DungeonCharacter)
        damage = self.hero.attempt_attack(target)
        self.assertEqual(damage, 15)
        mock_super_attack.assert_called_once_with(target)

    def test_str_representation(self):
        str_rep = str(self.hero)
        self.assertIn("Hero: Test Hero", str_rep)
        self.assertIn("Level: 1", str_rep)
        self.assertIn("HP: 100/100", str_rep)
        self.assertIn("XP: 0/100", str_rep)
        self.assertIn("Damage: 10-20", str_rep)
        self.assertIn("Hit Chance: 70%", str_rep)
        self.assertIn("Block Chance: 20%", str_rep)
        self.assertIn("No weapon equipped", str_rep)


if __name__ == "__main__":
    unittest.main()
