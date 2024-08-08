import pygame
from typing import Dict

from dungeon_adventure.config import RESOURCES_DIR
from dungeon_adventure.enums.room_types import Direction
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.services.dungeon_generator import DungeonGenerator
from dungeon_adventure.views.pygame.room.game_room import GameRoom
from dungeon_adventure.views.pygame.room.mini_map import MiniMap
from dungeon_adventure.views.pygame.sprites.py_player import PyPlayer


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
        self.background = pygame.image.load(f"{RESOURCES_DIR}/default_background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
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

        # Create player
        self.player_sprite_group = pygame.sprite.GroupSingle()
        self.player_sprite = PyPlayer()
        self.player_sprite.rect.center = self.current_room.rect.center
        # if self.player_sprite.rect is None:
        #     self.player_sprite.rect = self.player_sprite.image.get_rect()
        self.player_sprite_group.add(self.player_sprite)

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

        self.player_sprite_group.update(dt, self.current_room)
        self.game_rooms.update()  # Update all rooms (if needed)

        self.minimap.update(self.current_room, self.room_dict)

        player_pos = self.player_sprite.rect.center
        player_height = self.player_sprite.rect.height
        door_direction = self.current_room.get_door_at_position(player_pos, player_height)

        if door_direction:
            print(f"Colliding with {door_direction} door")
            self._handle_room_transition(door_direction)

    def _handle_room_transition(self, direction: Direction):
        current_dungeon_room = self.current_room.room
        next_dungeon_room = current_dungeon_room.connections[direction]
        if next_dungeon_room:
            next_room_name = next_dungeon_room.name
            self.current_room = self.room_dict[next_room_name]
            self._reposition_player(direction)

    def _reposition_player(self, entry_direction: Direction):
        opposite_direction = Room.opposite(entry_direction)
        door_hitbox = self.current_room.visuals.door_hitboxes[opposite_direction]

        # Get the room's center offset
        room_center_offset = self.current_room.visuals.get_center_offset()

        # Calculate the door's position relative to the room's center
        door_relative_pos = (
            door_hitbox.centerx + room_center_offset[0],
            door_hitbox.centery + room_center_offset[1]
        )

        # Set the player's position
        self.player_sprite.rect.center = door_relative_pos

        # Adjust the player's position to be just inside the room
        if opposite_direction == Direction.NORTH:
            self.player_sprite.rect.top = door_hitbox.bottom + room_center_offset[1]
        elif opposite_direction == Direction.SOUTH:
            self.player_sprite.rect.bottom = door_hitbox.top + room_center_offset[1]
        elif opposite_direction == Direction.WEST:
            self.player_sprite.rect.left = door_hitbox.right + room_center_offset[0]
        elif opposite_direction == Direction.EAST:
            self.player_sprite.rect.right = door_hitbox.left + room_center_offset[0]

    def draw(self):
        self.game_surface.blit(self.background, (0, 0))
        self.current_room.draw(self.game_surface)
        self.player_sprite_group.draw(self.game_surface)

        if self.debug_mode:
            self.current_room.draw_hitboxes(self.game_surface)
            self.player_sprite.draw_hitbox(self.game_surface)
            self.player_sprite.draw_debug_info(self.game_surface)
            self.draw_debug_info()

        scaled_surface = pygame.transform.scale(
            self.game_surface, (self.window_width, self.window_height)
        )

        self.screen.blit(scaled_surface, (0, 0))

        if not self.debug_mode:
            self.minimap.draw(self.screen)


    def draw_debug_info(self):
        font = pygame.font.Font(None, 15)
        y_offset = 10
        line_height = 20

        debug_info = [
            f"Debug Mode: ON",
            f"FPS: {self.fps:.2f}",
            f"Current Room: {self.current_room.room.name}",
            f"Room Image: {self.current_room.image_path.split('/')[-1]}",
            "Open Doors:",
        ]

        # Add open doors information
        for direction, connected_room in self.current_room.room.connections.items():
            if connected_room:
                debug_info.append(f"  {direction.name}: {connected_room.name}")

        # Add player position
        player_pos = self.player_sprite.rect.center
        debug_info.append(f"Player Position: {player_pos}")

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
        return True

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
