import os
from typing import Dict, List
from dungeon_adventure.enums.room_types import Direction


def _generate_door_code(open_doors: List[Direction]) -> str:
    code = ['X', 'X', 'X', 'X']
    direction_mapping = {
        Direction.NORTH: 0,
        Direction.SOUTH: 1,
        Direction.EAST: 2,
        Direction.WEST: 3
    }
    for door in open_doors:
        code[direction_mapping[door]] = door.name[0]
    print(''.join(code))
    return ''.join(code)


class RoomImageManager:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.image_cache: Dict[str, str] = {}

    def get_room_image(self, open_doors: List[Direction]) -> str:
        door_code = _generate_door_code(open_doors)

        if door_code in self.image_cache:
            return self.image_cache[door_code]

        image_path = os.path.join(self.base_path, f"room_{door_code}.png")

        if not os.path.exists(image_path):
            # Fallback to default image if specific configuration doesn't exist
            image_path = os.path.join(self.base_path, "room_XXXX.png")

        self.image_cache[door_code] = image_path
        return image_path

