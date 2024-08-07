import unittest
from unittest.mock import MagicMock, patch

from src.dungeon_adventure.models.characters import DungeonCharacter
from src.dungeon_adventure.models.characters.monster import Monster
from src.dungeon_adventure.models.items import Item


class TestMonster(unittest.TestCase):

    def setUp(self):
        self.monster = Monster("Test Monster", 100, 10, 20, 3, 70, 15, 5, 15, 100)

    def test_init(self):
        self.assertEqual(self.monster.name, "Test Monster")
        self.assertEqual(self.monster.max_hp, 100)
        self.assertEqual(self.monster.current_hp, 100)
        self.assertEqual(self.monster.base_min_damage, 10)
        self.assertEqual(self.monster.base_max_damage, 20)
        self.assertEqual(self.monster.attack_speed, 3)
        self.assertEqual(self.monster.base_hit_chance, 70)
        self.assertEqual(self.monster.heal_chance, 15)
        self.assertEqual(self.monster.min_heal, 5)
        self.assertEqual(self.monster.max_heal, 15)
        self.assertEqual(self.monster.xp_reward, 100)
        self.assertEqual(self.monster.loot, [])

    @unittest.skip("still need to update loot")
    def test_init_with_loot(self):
        item = Item("Test Item", "A test item")
        monster_with_loot = Monster(loot=[item])
        self.assertEqual(monster_with_loot.loot, [item])

    @patch("random.randint")
    def test_attempt_heal_successful(self, mock_randint):
        mock_randint.side_effect = [
            10,
            10,
        ]  # First for heal chance, second for heal amount
        self.monster.current_hp = 50  # Set HP lower to test healing
        heal_amount = self.monster.attempt_heal()
        self.assertEqual(heal_amount, 10)
        self.assertEqual(self.monster.current_hp, 60)

    @patch("random.randint")
    def test_attempt_heal_unsuccessful(self, mock_randint):
        mock_randint.return_value = 100  # Higher than heal_chance
        initial_hp = self.monster.current_hp
        heal_amount = self.monster.attempt_heal()
        self.assertEqual(heal_amount, 0)
        self.assertEqual(self.monster.current_hp, initial_hp)

    @unittest.skip("still need to update loot drop")
    def test_drop_loot(self):
        item1 = Item("Sword", "A sharp sword")
        item2 = Item("Shield", "A sturdy shield")
        self.monster.loot = [item1, item2]

        dropped_loot = self.monster.drop_loot()

        self.assertEqual(dropped_loot, [item1, item2])
        self.assertEqual(self.monster.loot, [])

    @patch.object(DungeonCharacter, "attempt_attack")
    @patch.object(Monster, "attempt_heal")
    def test_attempt_attack(self, mock_attempt_heal, mock_super_attack):
        target = MagicMock(spec=DungeonCharacter)
        mock_super_attack.return_value = 15

        damage_dealt = self.monster.attempt_attack(target)

        self.assertEqual(damage_dealt, 15)
        mock_super_attack.assert_called_once_with(target)
        mock_attempt_heal.assert_called_once()

    def test_create_custom_monster(self):
        custom_monster = Monster.create_custom_monster(
            name="Custom Monster",
            max_hp=200,
            base_min_damage=20,
            base_max_damage=30,
            attack_speed=4,
            base_hit_chance=80,
            heal_chance=20,
            min_heal=10,
            max_heal=20,
            xp_reward=150,
        )

        self.assertEqual(custom_monster.name, "Custom Monster")
        self.assertEqual(custom_monster.max_hp, 200)
        self.assertEqual(custom_monster.base_min_damage, 20)
        self.assertEqual(custom_monster.base_max_damage, 30)
        self.assertEqual(custom_monster.attack_speed, 4)
        self.assertEqual(custom_monster.base_hit_chance, 80)
        self.assertEqual(custom_monster.heal_chance, 20)
        self.assertEqual(custom_monster.min_heal, 10)
        self.assertEqual(custom_monster.max_heal, 20)
        self.assertEqual(custom_monster.xp_reward, 150)


if __name__ == "__main__":
    unittest.main()
