from src.characters.monster import Monster
from src.dungeon import Dungeon
from src.enums import Direction
from src.enums.item_types import WeaponType
from src.items.inventory_db import InventoryDatabase
from src.items.item_factory import ItemFactory


class DungeonGenerator:
    @staticmethod
    def generate_default_dungeon(db_path) -> Dungeon:
        item_factory = ItemFactory(db_path)
        dungeon = Dungeon()

        # Create all rooms
        room_names = [
            "Room 1 - Entrance Hall",
            "Room 2",
            "Room 3",
            "Room 4",
            "Room 5",
            "Room 6",
            "Room 7",
            "Room 8",
            "Room 9",
            "Room 10",
            "Room 11",
            "Room 12",
            "Room 13",
            "Room 14",
            "Room 15 - Exit Chamber",
        ]

        for room_name in room_names:
            dungeon.add_room(room_name)

        # Room Connections

        # Room 1
        dungeon.connect_rooms("Room 1 - Entrance Hall", Direction.NORTH, "Room 2")
        dungeon.connect_rooms("Room 1 - Entrance Hall", Direction.SOUTH, "Room 12")
        dungeon.connect_rooms("Room 1 - Entrance Hall", Direction.EAST, "Room 5")

        # Room 2
        dungeon.connect_rooms("Room 2", Direction.WEST, "Room 3")
        dungeon.connect_rooms("Room 2", Direction.EAST, "Room 4")

        # Room 4
        dungeon.connect_rooms("Room 4", Direction.NORTH, "Room 6")
        dungeon.connect_rooms("Room 4", Direction.SOUTH, "Room 5")
        dungeon.connect_rooms("Room 4", Direction.EAST, "Room 10")

        # Room 6
        dungeon.connect_rooms("Room 6", Direction.NORTH, "Room 7")
        dungeon.connect_rooms("Room 6", Direction.EAST, "Room 8")

        # Room 8
        dungeon.connect_rooms("Room 8", Direction.SOUTH, "Room 10")

        # Room 9
        dungeon.connect_rooms("Room 9", Direction.NORTH, "Room 10")

        # Room 10
        dungeon.connect_rooms("Room 10", Direction.EAST, "Room 11")

        # Room 12
        dungeon.connect_rooms("Room 12", Direction.SOUTH, "Room 13")

        # Room 13
        dungeon.connect_rooms("Room 13", Direction.SOUTH, "Room 14")

        # Room 14
        dungeon.connect_rooms("Room 14", Direction.SOUTH, "Room 15 - Exit Chamber")

        room2 = dungeon.get_room("Room 2")
        room2.add_monster(Monster("Robby Goblin"))
        room2.add_monster(Monster("Bobby Goblin"))

        room3 = dungeon.get_room("Room 3")
        room3.add_monster(Monster("Gobby King", max_hp=50, base_min_damage=15, base_max_damage=25))

        inventory_db = InventoryDatabase(db_path)
        item1 = item_factory.create_weapon("Sword", WeaponType.SWORD, 5, 5)
        inventory_db.add_item(item1, 1)

        return dungeon
