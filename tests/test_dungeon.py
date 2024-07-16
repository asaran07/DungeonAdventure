import pytest

from src.dungeon.dungeon import Dungeon
from src.items.item import Item


@pytest.fixture
def default_dungeon():
    return Dungeon()


@pytest.fixture
def another_dungeon():
    return Dungeon(10, 15)


@pytest.fixture
def item():
    return Item("Sword")


def test_dungeon_default_size(default_dungeon: Dungeon):
    assert default_dungeon.get_size() == (
        5,
        5,
    )  # The default is 5 for both width and height.


def test_get_room(default_dungeon: Dungeon):
    assert isinstance(default_dungeon.get_room(1, 1), Room)
