from src.dungeon import Room
from src.enums import Direction

room = Room("Main Entrance")
room2 = Room("Lobby")
room.connect(Direction.NORTH, room2)

print(room)