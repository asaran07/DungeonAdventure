from src.dungeon import Room
from src.enums import Direction
from src.items.item import Item

room = Room("Main Entrance")
room2 = Room("Lobby")
room.connect(Direction.NORTH, room2)
room.add_item(Item("Sword"))
room.add_item(Item("Healing Potion"))

print(room)
