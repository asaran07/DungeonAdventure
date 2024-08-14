import random
from dungeon_adventure.enums.item_types import PillarType, PotionType, WeaponType
from dungeon_adventure.enums.room_types import Direction, RoomType
from dungeon_adventure.models.dungeon.dungeon import Dungeon
from dungeon_adventure.services.item_factory import ItemFactory
from src.dungeon_adventure.models.characters.monster import Monster


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

        monster_instance = Monster()

        room1 = dungeon.get_room("Room 1 - Entrance Hall")
        room1.room_type = RoomType.ENTRANCE

        room2 = dungeon.get_room("Room 2")
        random_monster = monster_instance.generate_random_monster()
        random_monster_2 = monster_instance.generate_random_monster()
        room2.add_monster(random_monster)
        room2.add_monster(random_monster_2)
        room2.add_item(
            item_factory.create_pillar(
                PillarType.ENCAPSULATION,
                "Encapsulation Pillar",
                "A encapsulated pillar",
                10,
            )
        )
        room2.add_item(
            item_factory.create_potion("Healing Potion", PotionType.HEALING, 15, 2)
        )

        room3 = dungeon.get_room("Room 3")
        room3.add_item(item_factory.create_rope())

        room6 = dungeon.get_room("Room 6")
        room6.room_type = RoomType.PIT

        room7 = dungeon.get_room("Room 7")
        random_monster_5 = monster_instance.generate_random_monster()
        random_monster_6 = monster_instance.generate_random_monster()
        room7.add_monster(random_monster_5)
        room7.add_monster(random_monster_6)
        room7.add_item(
            item_factory.create_pillar(
                PillarType.INHERITANCE,
                "Inheritance Pillar",
                "An inheritance pillar",
                10,
            )
        )

        room8 = dungeon.get_room("Room 8")
        random_monster_12 = monster_instance.generate_random_monster()
        room8.add_monster(random_monster_12)
        room8.add_item(
            item_factory.create_potion("Healing Potion", PotionType.HEALING, 15, 2)
        )

        room9 = dungeon.get_room("Room 9")
        random_monster_7 = monster_instance.generate_random_monster()
        random_monster_8 = monster_instance.generate_random_monster()
        room9.add_monster(random_monster_7)
        room9.add_monster(random_monster_8)
        room9.add_item(
            item_factory.create_pillar(
                PillarType.POLYMORPHISM,
                "Polymorphism Pillar",
                "A polymorphism pillar",
                10,
            )
        )

        room10 = dungeon.get_room("Room 10")
        room10.add_item(
            item_factory.create_potion("Vision Potion", PotionType.VISION, 0, 2)
        )

        room11 = dungeon.get_room("Room 11")
        random_monster_13 = monster_instance.generate_random_monster()
        room11.add_monster(random_monster_13)

        room12 = dungeon.get_room("Room 12")
        room12.add_item(
            item_factory.create_potion("Healing Potion", PotionType.HEALING, 15, 2)
        )
        room12.add_item(
            item_factory.create_weapon("Rusty Sword", WeaponType.SWORD, 10, 7, 100)
        )

        room13 = dungeon.get_room("Room 13")
        random_monster_3 = monster_instance.generate_random_monster()
        random_monster_4 = monster_instance.generate_random_monster()
        room13.add_monster(random_monster_3)
        room13.add_monster(random_monster_4)
        room13.add_item(item_factory.create_rope())
        room13.add_item(
            item_factory.create_pillar(
                PillarType.ABSTRACTION, "Abstraction Pillar", "A pillar that is a bit abstract.", 5
            )
        )

        room14 = dungeon.get_room("Room 14")
        room14.room_type = RoomType.PIT
        room14.add_item(
            item_factory.create_pillar(PillarType.ENCAPSULATION, "Encapsulation Pillar", "A encap pillar", 5))
        room14.add_item(
            item_factory.create_pillar(PillarType.INHERITANCE, "Inheritance Pillar", "A inh pillar", 5))
        room14.add_item(
            item_factory.create_pillar(PillarType.POLYMORPHISM, "Polymorphism Pillar", "A poly pillar", 5))

        room15 = dungeon.get_room("Room 15 - Exit Chamber")
        room15.set_room_type(RoomType.EXIT)
        random_monster_9 = monster_instance.generate_random_monster()
        random_monster_10 = monster_instance.generate_random_monster()
        random_monster_11 = monster_instance.generate_random_monster()
        room15.add_monster(random_monster_9)
        room15.add_monster(random_monster_10)
        room15.add_monster(random_monster_11)

        return dungeon
