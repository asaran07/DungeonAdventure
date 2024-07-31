from src.dungeon import Dungeon, Room
from src.enums import Direction, RoomType
from src.items.weapon import Weapon
from src.enums.item_types import WeaponType
from src.characters.monster import Monster


class DungeonGenerator:
    @staticmethod
    def generate_default_dungeon() -> Dungeon:
        dungeon = Dungeon()
        dungeon.add_room("Room 1")
        dungeon.get_room("Room 1").add_item(Weapon("Rusty Dagger", "A rusty dagger", 0.5, WeaponType.DAGGER, 1, 5))
        dungeon.add_and_connect_room("Room 2", "Room 1", Direction.NORTH)
        dungeon.add_and_connect_room("Room 3", "Room 2", Direction.EAST)
        dungeon.add_and_connect_room("Room 4", "Room 3", Direction.EAST)
        dungeon.add_and_connect_room("Room 5", "Room 3", Direction.NORTH)

        room2 = dungeon.get_room("Room 2")
        if room2:
            room2.add_monster(Monster(name="Robby Goblin", base_min_damage=1, base_max_damage=4))
            room2.add_monster(Monster(name="Bobby Goblin", base_min_damage=3, base_max_damage=7))

        return dungeon


