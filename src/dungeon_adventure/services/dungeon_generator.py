from dungeon_adventure.enums.item_types import PillarType, PotionType, WeaponType
from dungeon_adventure.enums.room_types import Direction, RoomType
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.models.dungeon.dungeon import Dungeon
from dungeon_adventure.services.item_factory import ItemFactory


class DungeonGenerator:
    @staticmethod
    def generate_default_dungeon() -> Dungeon:
        item_factory = ItemFactory()
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

        room1 = dungeon.get_room("Room 1 - Entrance Hall")
        room1.room_type = RoomType.ENTRANCE

        room2 = dungeon.get_room("Room 2")
        room2.add_monster(Monster("Robby Goblin"))
        room2.add_monster(Monster("Bobby Goblin"))

        room3 = dungeon.get_room("Room 3")
        room3.add_monster(
            Monster("Gobby King", max_hp=50, base_min_damage=15, base_max_damage=25)
        )

        room12 = dungeon.get_room("Room 12")
        room12.add_item(
            item_factory.create_pillar(
                PillarType.ABSTRACTION, "Abstraction Pillar", "A abstract pillar", 5
            )
        )
        room12.add_item(
            item_factory.create_pillar(
                PillarType.ENCAPSULATION,
                "Encapsulation Pillar",
                "A encapsulated pillar",
                10,
            )
        )

        room12.add_item(
            item_factory.create_weapon("Rusty Sword", WeaponType.SWORD, 10, 7, 100)
        )
        room12.add_item(
            item_factory.create_potion("Healing Potion", PotionType.HEALING, 15, 2)
        )

        room15 = dungeon.get_room("Room 15 - Exit Chamber")
        room15.set_room_type(RoomType.EXIT)

        return dungeon
