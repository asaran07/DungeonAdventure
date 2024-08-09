import pygame
from typing import Dict

from dungeon_adventure.config import RESOURCES_DIR
from dungeon_adventure.enums.room_types import Direction
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.services.dungeon_generator import DungeonGenerator
from dungeon_adventure.views.pygame.room.game_room import GameRoom
from dungeon_adventure.views.pygame.room.inventory_display import InventoryDisplay
from dungeon_adventure.views.pygame.room.mini_map import MiniMap
from dungeon_adventure.views.pygame.room.room_items_display import RoomItemsDisplay
from dungeon_adventure.views.pygame.sprites.composite_player import CompositePlayer
from dungeon_adventure.views.pygame.sprites.py_player import PyPlayer
from src.dungeon_adventure.views.pygame.room.controls_display import ControlsDisplay


class Application:
    def __init__(self, width=480, height=270):
        pygame.init()
        pygame.display.set_caption("Dungeon Adventure")
        self.width = width
        self.height = height
        self.scale_factor = 3
        self.window_width = self.width * self.scale_factor
        self.window_height = self.height * self.scale_factor
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.background = pygame.image.load(
            f"{RESOURCES_DIR}/default_background.png"
        ).convert_alpha()
        self.background = pygame.transform.scale(
            self.background, (self.width, self.height)
        )
        self.game_surface = pygame.Surface((self.width, self.height))

        self.debug_mode = False
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.fps_update_time = 0

        self.dungeon = DungeonGenerator.generate_default_dungeon()
        self.game_rooms = pygame.sprite.Group()
        self.room_dict: Dict[str, GameRoom] = self._create_game_rooms()
        self.current_room = self._get_starting_room()

        self.minimap = MiniMap(self.window_width, self.window_height)
        self.inventory_display = InventoryDisplay(
            self.window_width, self.window_height, self.scale_factor
        )
        self.room_items_display = RoomItemsDisplay(self.window_width)
        self.controls_display = ControlsDisplay(
            self.window_width, self.window_height, self.scale_factor
        )

        # Create player
        self.player = CompositePlayer("Player 1")
        self.player.py_player.rect.center = self.current_room.rect.center
        self.player_sprite_group = pygame.sprite.GroupSingle(self.player.sprite)
        # if self.player_sprite.rect is None:
        #     self.player_sprite.rect = self.player_sprite.image.get_rect()
        self.player_sprite_group.add(self.player.py_player)

        self.scaled_surface = pygame.Surface((self.window_width, self.window_height))

    def _create_game_rooms(self) -> Dict[str, GameRoom]:
        room_dict = {}
        for room_name, room in self.dungeon.rooms.items():
            game_room = GameRoom(room)
            game_room.rect.center = (self.width // 2, self.height // 2)
            self.game_rooms.add(game_room)
            room_dict[room_name] = game_room
        return room_dict

    def _get_starting_room(self) -> GameRoom:
        starting_room_name = next(iter(self.dungeon.rooms.keys()))
        return self.room_dict[starting_room_name]

    def update(self):
        dt = self.clock.tick(60)
        current_time = pygame.time.get_ticks()

        if current_time - self.fps_update_time > 1000:  # Update FPS every second
            self.fps = self.clock.get_fps()
            self.fps_update_time = current_time

        self.player.update(dt, self.current_room)
        self.game_rooms.update()  # Update all rooms (if needed)

        self.minimap.update(self.current_room, self.room_dict)
        self.room_items_display.update(self.current_room.room)

        player_pos = self.player.rect.center
        player_height = self.player.rect.height

        door_direction = self.current_room.get_door_at_position(
            player_pos, player_height
        )

        if door_direction:
            print(f"Colliding with {door_direction} door")
            self._handle_room_transition(door_direction)

    def _handle_room_transition(self, direction: Direction):
        current_dungeon_room = self.current_room.room
        next_dungeon_room = current_dungeon_room.connections[direction]
        if next_dungeon_room:
            next_room_name = next_dungeon_room.name
            self.current_room = self.room_dict[next_room_name]
            self.player.current_room = (
                next_room_name  # update the player's location as well
            )
            self._reposition_player(direction)

    def _reposition_player(self, entry_direction: Direction):
        opposite_direction = Room.opposite(entry_direction)
        door_hitbox = self.current_room.visuals.door_hitboxes[opposite_direction]

        # Get the room's center offset
        room_center_offset = self.current_room.visuals.get_center_offset()

        # Calculate the door's position relative to the room's center
        door_relative_pos = (
            door_hitbox.centerx + room_center_offset[0],
            door_hitbox.centery + room_center_offset[1],
        )

        # Set the player's position
        self.player.rect.center = door_relative_pos

        # Adjust the player's position to be just inside the room
        if opposite_direction == Direction.NORTH:
            self.player.rect.top = door_hitbox.bottom + room_center_offset[1]
        elif opposite_direction == Direction.SOUTH:
            self.player.rect.bottom = door_hitbox.top + room_center_offset[1]
        elif opposite_direction == Direction.WEST:
            self.player.rect.left = door_hitbox.right + room_center_offset[0]
        elif opposite_direction == Direction.EAST:
            self.player.rect.right = door_hitbox.left + room_center_offset[0]

    def draw(self):
        self.game_surface.blit(self.background, (0, 0))
        self.current_room.draw(self.game_surface)
        self.player_sprite_group.draw(self.game_surface)

        if self.debug_mode:
            self.current_room.draw_hitboxes(self.game_surface)
            self.player.draw_hitbox(self.game_surface)
            self.player.draw_debug_info(self.game_surface)
            self.draw_debug_info()

        scaled_surface = pygame.transform.scale(
            self.game_surface, (self.window_width, self.window_height)
        )

        self.screen.blit(scaled_surface, (0, 0))

        if not self.debug_mode:
            self.minimap.draw(self.screen)
            self.inventory_display.draw(self.screen, self.player.inventory)
            self.room_items_display.draw(self.screen)
            self.controls_display.draw(self.screen)

    def draw_debug_info(self):
        font = pygame.font.Font(None, 15)
        y_offset = 10
        line_height = 20

        debug_info = [
            f"Debug Mode: ON",
            f"FPS: {self.fps:.2f}",
            f"Current Room: {self.current_room.room.name}",
            f"Room Type: {self.current_room.room.room_type}",
            f"Room Image: {self.current_room.image_path.split('/')[-1]}",
            "Open Doors:",
        ]

        # Add open doors information
        for direction, connected_room in self.current_room.room.connections.items():
            if connected_room:
                debug_info.append(f"  {direction.name}: {connected_room.name}")

        # Add player position
        player_pos = self.player.rect.center
        debug_info.append(f"Player Position: {player_pos}")
        debug_info.append(f"Player Name: {self.player.name}")
        debug_info.append(
            f"Player HP: {self.player.hero.current_hp}/{self.player.hero.max_hp}"
        )

        for i, info in enumerate(debug_info):
            debug_surface = font.render(info, True, (255, 255, 255))
            self.game_surface.blit(debug_surface, (10, y_offset + i * line_height))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.debug_mode = not self.debug_mode
                    print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
                elif event.key == pygame.K_t:  # 'T' for Take
                    self.handle_take_item()
                elif event.key == pygame.K_x:  # 'D' for Drop
                    self.handle_drop_item()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click is inside the inventory area
                if self.inventory_display.is_point_inside(event.pos):
                    # Handle inventory interaction
                    pass
        return True

    def handle_take_item(self, pos=None):
        if pos:
            item = self.room_items_display.get_item_at_position(pos)
        else:
            # Take the first item in the room if no position is specified
            item = (
                self.current_room.room.items[0]
                if self.current_room.room.items
                else None
            )

        if item:
            try:
                self.player.inventory.add_item(item)
                self.current_room.room.remove_item(item)
                print(f"Took {item.name}")
            except Exception as e:
                print(f"Couldn't take {item.name}: {str(e)}")

    def handle_drop_item(self):
        # For simplicity, drop the last item in the inventory
        if self.player.inventory._items:
            item_id, (item, quantity) = self.player.inventory._items.popitem()
            self.current_room.room.add_item(item)
            print(f"Dropped {item.name}")
        else:
            print("No items to drop")

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    app = Application()
    app.run()
