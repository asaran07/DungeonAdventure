from src.characters.monster import Monster
from src.dungeon import Dungeon
from src.enums import Direction
from src.enums.item_types import WeaponType, PotionType
from src.items.item_factory import ItemFactory


class DungeonGenerator:
    @staticmethod
    def generate_default_dungeon() -> Dungeon:
        item_factory = ItemFactory()

        dungeon = Dungeon()
        dungeon.add_room("Room 1")
        dungeon.add_and_connect_room("Room 2", "Room 1", Direction.NORTH)
        dungeon.add_and_connect_room("Room 3", "Room 2", Direction.EAST)
        dungeon.add_and_connect_room("Room 4", "Room 3", Direction.EAST)
        dungeon.add_and_connect_room("Room 5", "Room 3", Direction.NORTH)

        room1 = dungeon.get_room("Room 1")
        if room1:
            room1.add_item(item_factory.create_potion("Healing Potion", PotionType.HEALING, 15, 2.0))

        room2 = dungeon.get_room("Room 2")
        if room2:
            room2.add_item(item_factory.create_weapon("Rusty Sword", WeaponType.SWORD, 10, 5.0))
            room2.add_monster(Monster(name="Robby Goblin", xp_reward=20))
            room2.add_monster(Monster(name="Bobby Goblin", xp_reward=35))

        room3 = dungeon.get_room("Room 3")
        if room3:
            room3.add_monster(
                Monster(name="Gobby King", base_min_damage=7, base_max_damage=15, xp_reward=60),
            )

        return dungeon
