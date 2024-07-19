import pytest

from src.dungeon.room import Room
from src.enums.room_types import Direction, RoomType


@pytest.fixture
def new_room():
    return Room("Room1")


def test_default_room_type(new_room: Room):
    assert new_room.room_type == RoomType.NORMAL


def test_room(new_room):
    assert isinstance(new_room, Room)


def test_available_open_directions():
    room1 = Room("room1")
    room2 = Room("room2")
    room3 = Room("room3")
    room1.connect(Direction.WEST, room2)
    room1.connect(Direction.NORTH, room3)

    expected_directions_and_rooms = [(Direction.WEST, room2), (Direction.NORTH, room3)]
    assert set(expected_directions_and_rooms) == set(room1.get_open_gates())


@pytest.mark.skip(reason="Not implemented yet")
def test_unmade_room_feature():
    pass


def test_invalid_item():
    # with pytest.raises(
    #    TypeError
    # ):  # This is like if the class raises a certain exception
    # But I am commenting this out to avoide LSP errors
    # Room(RoomType.NORMAL).add_item("Not an item")
    pass


def test_room_items(new_room):
    assert len(new_room.items) == 0, "Room should start with no items"


@pytest.mark.xfail
def test_known_bug():
    assert 1 == 2  # This will fail but the whole test run won't fail
