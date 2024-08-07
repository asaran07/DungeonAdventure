import pytest

from src.dungeon_adventure.enums.room_types import Direction
from src.dungeon_adventure.models.dungeon import Dungeon
from src.dungeon_adventure.models.dungeon.room import Room


@pytest.fixture
def empty_room():
    return Room("Empty")


@pytest.fixture
def simple_dungeon():
    dungeon = Dungeon()
    dungeon.add_room("A")
    dungeon.add_room("B")
    return dungeon


def test_room_creation(empty_room):
    assert empty_room.name == "Empty"
    assert all(connection is None for connection in empty_room.connections.values())


def test_room_connection(empty_room):
    other_room = Room("Other")
    # Connect empty_room's north direction to other_room
    assert empty_room.connect(Direction.NORTH, other_room)

    # Check if empty_room's north direction leads to the other_room
    assert empty_room.connections[Direction.NORTH] == other_room

    # Check if other_room's south direction leads back to empty_room
    assert other_room.connections[Direction.SOUTH] == empty_room


def test_room_connection_fails_if_already_connected(empty_room):
    # Make two rooms
    room1 = Room("Room1")
    room2 = Room("Room2")

    # Connect empty_room's north side to room1
    empty_room.connect(Direction.NORTH, room1)

    # Try connecting empty_room's north side to room2
    assert not empty_room.connect(Direction.NORTH, room2)

    # Check if empty_room is still connected to the original room1
    assert empty_room.connections[Direction.NORTH] == room1


def test_dungeon_add_room(simple_dungeon):
    # Check if A and B exist in the dungeon and dungeon size is two
    assert "A" in simple_dungeon.rooms
    assert "B" in simple_dungeon.rooms
    assert len(simple_dungeon.rooms) == 2


def test_dungeon_connect_nonexistent_room(simple_dungeon):
    room_a = simple_dungeon.rooms["A"]
    room_c = Room("C")  # Not added to the dungeon
    assert simple_dungeon.connect_rooms(room_a, Direction.NORTH, room_c)
    # The connection is made, but room C is not added to the dungeon
    assert "C" not in simple_dungeon.rooms
