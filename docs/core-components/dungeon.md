# Core Components - Dungeon

## Dungeon Class

Location: `src/dungeon/dungeon.py`

The `Dungeon` class represents the game world structure.

### Key Attributes

- `rooms`: Dict[str, Room] - Stores all rooms in the dungeon
- `entrance_room`: Optional[Room] - The starting room for the player

### Important Methods

- `add_room(name: str) -> Room`: Creates and adds a new room to the dungeon
- `connect_rooms(room1_name: str, direction: Direction, room2_name: str) -> bool`: Connects two rooms in the specified direction
- `get_room(room_name: str) -> Room`: Retrieves a room by its name

## Room Class

Location: `src/dungeon/room.py`

The `Room` class represents individual locations within the dungeon.

### Key Attributes Room

- `name`: str - Unique identifier for the room
- `room_type`: RoomType - Type of room (e.g., NORMAL, ENTRANCE, EXIT)
- `connections`: Dict[Direction, Optional[Room]] - Connections to other rooms
- `items`: List[Item] - Items present in the room

### Important Methods Room

- `connect(direction: Direction, other_room: Room) -> bool`: Connects this room to another in the specified direction
- `add_item(item: Item)`: Adds an item to the room
- `remove_item(item: Item)`: Removes an item from the room

## Dungeon Generation Algorithm

The dungeon is generated in the `make_rooms` method of the `GameModel` class:

1. Create the entrance room
2. Recursively add and connect rooms
3. Place items and monsters in rooms
4. Set the entrance and exit rooms
