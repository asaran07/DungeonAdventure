import pytest

from src.dungeon.room import Room
from src.enums.room_types import RoomType


@pytest.fixture
def new_room():
    return Room(RoomType.NORMAL)


def test_room(new_room):
    assert isinstance(new_room, Room)


@pytest.mark.skip(reason="Not implemented yet")
def test_unmade_room_feature():
    pass


def test_invalid_item():
    with pytest.raises(
        TypeError
    ):  # This is like if the class raises a certain exception
        # But I am commenting this out to avoide LSP errors
        # Room(RoomType.NORMAL).add_item("Not an item")
        pass


def test_room_items(new_room):
    assert len(new_room.items) == 0, "Room should start with no items"


@pytest.mark.xfail
def test_known_bug():
    assert 1 == 2  # This will fail but the whole test run won't fail
