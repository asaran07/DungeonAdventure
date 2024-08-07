from unittest.mock import Mock

import pytest

from dungeon_adventure.controllers.combat_controller import CombatController
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.views.console.console_view import ConsoleView
from src import GameModel


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
    return CombatController(mock_game_model, view)
