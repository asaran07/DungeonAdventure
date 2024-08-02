from unittest.mock import Mock

import pytest

from src.characters import Player
from src.characters.monster import Monster
from src.combat.combat_handler import CombatHandler
from src.dungeon.room import Room
from src.game.dungeon_adventure import GameModel
from src.views.console_view import ConsoleView


@pytest.fixture
def mock_game_model():
    player = Player("Test Player")
    dungeon = Mock()
    return GameModel(player, dungeon)


@pytest.fixture
def mock_room():
    room = Room("Test Room")
    monster = Monster(
        "Test Monster", max_hp=50, base_min_damage=5, base_max_damage=10, xp_reward=100
    )
    room.add_monster(monster)
    return room


@pytest.fixture
def combat_handler(mock_game_model):
    view = ConsoleView()
    return CombatHandler(mock_game_model, view)
