import pytest
from Item import Item
from src.Dungeon import Dungeon


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
    )  # The deafult is 5 for both width and height.
