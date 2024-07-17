from unittest import mock
import pytest
import random

from src.characters.dungeon_character import DungeonCharacter

@pytest.fixture
def dungeon_character():
    return DungeonCharacter()

#trying to learn how to use mock to test the random numbers, this section is not complete
def test_attack():
    pass
    # with mock.patch ('dungeon_character.random') as m:
    #     m.random.return_value = 20
    #     self assertEqual(dungeon_character.attack(), 20)

def test_lose_health():
    dungeon_character_one = DungeonCharacter("Skeleton", 20,
                                             2, 5,
                                             1, 80 )
    dungeon_character_one.lose_health(15)
    assert dungeon_character_one.hp == 5