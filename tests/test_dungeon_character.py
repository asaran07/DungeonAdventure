import pytest
import random
from random import Random
import unittest
from unittest.mock import patch

from src.characters.dungeon_character import DungeonCharacter


@pytest.fixture
def dungeon_character():
    return DungeonCharacter()


# def set_up(self):
#     self.random_hit_roll = Random(222)
#     self.random_damage = Random(222)

# @patch('src.characters.dungeon_character.DungeonCharacter.random_hit_roll')
#trying to learn how to use mock to test the random numbers, this section is not complete
def test_attack():
    pass

# @patch('src.characters.dungeon_character.DungeonCharacter.random_damage')
def test_lose_health():
    pass
    # random_damage.randint.mock_side_effect = self.random_damage.randint
    #
    # dungeon_character_one = DungeonCharacter("Skeleton", 20,
    #                                          2, 5,
    #                                          1, 80)
    # dungeon_character_one.lose_health()
    # self.assert dungeon_character_one.hp == 15
