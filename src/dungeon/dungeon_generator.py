from src.dungeon import Dungeon
from src.enums import Direction
from src.items.weapon import Weapon
from src.enums.item_types import WeaponType
from src.characters.monster import Monster


class DungeonGenerator:
    @staticmethod
    def generate_default_dungeon() -> Dungeon:
        dungeon = Dungeon()

        dungeon.add_room("Room 1")
        dungeon.add_and_connect_room("Room 2", "Room 1", Direction.NORTH)
        dungeon.add_and_connect_room("Room 3", "Room 2", Direction.EAST)
        dungeon.add_and_connect_room("Room 4", "Room 3", Direction.EAST)
        dungeon.add_and_connect_room("Room 5", "Room 3", Direction.NORTH)

        room1 = dungeon.get_room("Room 1")
        if room1:
            room1.add_item(Weapon("Basic Sword", "A basic sword", 1, WeaponType.SWORD, 2, 10))

        room2 = dungeon.get_room("Room 2")
        if room2:
            room2.add_monster(Monster())

        return dungeon


