from src.dungeon import Room
from src.enums import Direction
from src.enums.item_types import ItemType, WeaponType
from src.items.weapon import Weapon

room = Room("Main Entrance")
room2 = Room("Lobby")
room.connect(Direction.NORTH, room2)
sword = Weapon("Excalibur", ItemType.WEAPON, "A legendary sword", 5.0, WeaponType.SWORD, 100)

print(room)
