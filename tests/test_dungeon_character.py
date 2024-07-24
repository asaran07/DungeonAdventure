import unittest
from unittest.mock import patch
from src.characters.dungeon_character import DungeonCharacter

class TestDungeonCharacter(unittest.TestCase):

    def setUp(self):
        self.character = DungeonCharacter("Test Character", 100, 10,
                                          20, 2, 70)

    def test_init(self):
        self.assertEqual(self.character.name, "Test Character")
        self.assertEqual(self.character.hp, 100)
        self.assertEqual(self.character.min_damage, 10)
        self.assertEqual(self.character.max_damage, 20)
        self.assertEqual(self.character.attack_speed, 2)
        self.assertEqual(self.character.chance_to_hit, 70)

    @patch('random.randint')
    def test_attack_hit(self, mock_randint):
        mock_randint.return_value = 50  # Simulating a die roll that hits
        opponent = DungeonCharacter("Opponent", 100)
        with patch.object(opponent, 'lose_health') as mock_lose_health:
            self.character.attack(opponent)
            mock_lose_health.assert_called_once()

    @patch('random.randint')
    def test_attack_miss(self, mock_randint):
        mock_randint.return_value = 80  # Simulating a die roll that misses
        opponent = DungeonCharacter("Opponent", 100)
        with patch.object(opponent, 'lose_health') as mock_lose_health:
            self.character.attack(opponent)
            mock_lose_health.assert_not_called()

    def test_attack_when_ko(self):
        self.character.hp = 0
        opponent = DungeonCharacter("Opponent", 100)
        with patch.object(opponent, 'lose_health') as mock_lose_health:
            self.character.attack(opponent)
            mock_lose_health.assert_not_called()

    @patch('random.randint')
    def test_lose_health(self, mock_randint):
        mock_randint.return_value = 15  # Simulating a damage roll
        initial_hp = self.character.hp
        self.character.lose_health()
        self.assertEqual(self.character.hp, initial_hp - 15)

    @patch('random.randint')
    def test_lose_health_ko(self, mock_randint):
        mock_randint.return_value = 150  # Simulating a damage roll greater than current HP
        self.character.lose_health()
        self.assertEqual(self.character.hp, 0)

if __name__ == '__main__':
    unittest.main()