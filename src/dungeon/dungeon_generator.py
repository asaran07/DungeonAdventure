from src.characters.monster import Monster
from src.dungeon import Dungeon
from src.enums import Direction
from src.enums.item_types import WeaponType
from src.items.weapon import Weapon


class DungeonGenerator:
    @staticmethod
    def generate_default_dungeon() -> Dungeon:
        dungeon = Dungeon()
        dungeon.add_room("Room 1")
        dungeon.add_and_connect_room("Room 2", "Room 1", Direction.NORTH)
        dungeon.add_and_connect_room("Room 3", "Room 2", Direction.EAST)
        dungeon.add_and_connect_room("Room 4", "Room 3", Direction.EAST)
        dungeon.add_and_connect_room("Room 5", "Room 3", Direction.NORTH)

        room2 = dungeon.get_room("Room 2")
        if room2:
            room2.add_monster(Monster(name="Robby Goblin"))
            room2.add_monster(Monster(name="Bobby Goblin"))

        room3 = dungeon.get_room("Room 3")
        if room3:
            room3.add_monster(
                Monster(name="Gobby King", base_min_damage=5, base_max_damage=10)
            )

        return dungeon
