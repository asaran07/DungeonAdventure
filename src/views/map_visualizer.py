from typing import List, Dict, Optional, Tuple, Set
from src.dungeon.room import Room
from src.enums.room_types import Direction


class MapVisualizer:
    def __init__(self, dungeon):
        self.dungeon = dungeon
        # Make a dictionary like this [[room coordinates], [room]] to store the coordinates of our rooms
        # as key and the room itself for the value.
        self.grid: Dict[Tuple[int, int], Room] = {}
        # Set of already explored rooms, using coordinates (x, y)
        self.explored_rooms: Set[Tuple[int, int]] = set()

    def initialize(self):
        """Initialize the map visualizer after the dungeon has been set up."""
        self._assign_coordinates()

    def _assign_coordinates(self):
        start_room = self.dungeon.get_entrance_room()
        if start_room is None:
            # hopefully we won't get to this point
            print("Warning: Dungeon has not been initialized yet. Map will be empty.")
            return
        self._assign_room_coordinates(start_room, 0, 0, set())

    def _assign_room_coordinates(self, current_room: Room, x: int, y: int, visited: set):
        """depth first search baby!!"""
        # No infinite loop on interconnected rooms
        if current_room in visited:
            return
        # Mark the room as visited
        visited.add(current_room)
        # Then add that room to our grid using coordinates
        self.grid[(x, y)] = current_room
        # Go through all other connected rooms of current room
        for direction, connected_room in current_room.get_open_gates():
            if connected_room:
                dx, dy = direction.get_coordinate_change()
                new_x, new_y = x + dx, y + dy
                self._assign_room_coordinates(connected_room, new_x, new_y, visited)

    # I'll add more comments soon enough lol
    def update_explored_rooms(self, current_room: Room):
        current_coords = next(coords for coords, room in self.grid.items() if room == current_room)
        self.explored_rooms.add(current_coords)

        for direction in Direction:
            if current_room.connections[direction]:
                x, y = current_coords
                dx, dy = direction.get_coordinate_change()
                new_coords = (x + dx, y + dy)
                self.explored_rooms.add(new_coords)

    def generate_map(self, current_room: Room) -> List[str]:
        if not self.grid:
            return ["Map is not available yet."]

        self.update_explored_rooms(current_room)

        # Theres probably ways to make all this way more efficient and consist
        visible_rooms = self.explored_rooms
        min_x = min(x for x, _ in visible_rooms)
        max_x = max(x for x, _ in visible_rooms)
        min_y = min(y for _, y in visible_rooms)
        max_y = max(y for _, y in visible_rooms)

        map_lines = []
        for y in range(min_y, max_y + 1):
            room_line = []
            for x in range(min_x, max_x + 1):
                if (x, y) in visible_rooms:
                    room = self.grid[(x, y)]
                    if room == current_room:
                        room_char = 'X'
                    elif room.is_explored:
                        room_char = 'O'
                    else:
                        room_char = ' '
                    room_line.append(f'[{room_char}]')
                else:
                    room_line.append('   ')
            map_lines.append(''.join(room_line))

        return map_lines

    def display_map(self, current_room: Room):
        map_lines = self.generate_map(current_room)
        print("\nDungeon Map:")
        for line in map_lines:
            print(line)
        # print("\nLegend:")
        # print("[X] - Current Room")
        # print("[O] - Explored Room")
        # print("[ ] - Unexplored Room")
