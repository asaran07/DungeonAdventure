import os

import pygame

from dungeon_adventure.config import RESOURCES_DIR
from dungeon_adventure.enums.room_types import Direction
from dungeon_adventure.game_model import GameModelError
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.models.player import Player
from dungeon_adventure.services.dungeon_generator import DungeonGenerator
from dungeon_adventure.views.pygame.room.game_room import GameRoom
from dungeon_adventure.views.pygame.sprites.py_player import PyPlayer
from src import GameModel

class Application:
    def __init__(self, width=480, height=270):
        pygame.init()
        self.width = width
        self.height = height
        self.scale_factor = 3
        self.window_width = self.width * self.scale_factor
        self.window_height = self.height * self.scale_factor
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.background = pygame.image.load("../resources/default_background.png")
        self.background = pygame.transform.scale(
            self.background, (self.width, self.height)
        )
        self.game_surface = pygame.Surface((self.width, self.height))
        pygame.display.set_caption("Dungeon Adventure")

        self.debug_mode = False

        # Create game rooms
        self.rooms = pygame.sprite.Group()
        test_room = Room("Test Room")
        test_room2 = Room("Test Room 2")
        test_room3 = Room("Test Room 3")
        test_room4 = Room("Test Room 4")
        test_room.connect(Direction.NORTH, test_room2)
        test_room.connect(Direction.EAST, test_room3)
        test_room.connect(Direction.WEST, test_room4)
        room1 = GameRoom(test_room, os.path.join(RESOURCES_DIR, 'basic_room.png'))
        room1.rect.center = (self.width // 2, self.height // 2)
        self.rooms.add(room1)

        # Create player
        self.player = pygame.sprite.GroupSingle()
        self.player_sprite = PyPlayer()
        self.player_sprite.rect.center = room1.rect.center
        self.player.add(self.player_sprite)

        self.clock = pygame.time.Clock()

    def _create_rooms(self):
        test_room = Room("Room 1")

        # room1.rect.center = (self.width // 2, self.height // 2)

        # Add more rooms as needed

    def _get_starting_room(self):
        # Return the starting room (e.g., the entrance hall)
        return next(iter(self.rooms.sprites()))

    def update(self):
        dt = self.clock.tick(60)
        current_room = next(iter(self.rooms.sprites()))
        self.player_sprite.update(dt, current_room.floor_rect)

        # Check for room transitions
        # door_direction = current_room.get_door_at_position(self.player_sprite.rect.center)
        # if door_direction:
        #     self._handle_room_transition(door_direction)

    def _get_current_room(self):
        # This method should return the room the player is currently in
        # For now, we'll just return the first room
        return next(iter(self.rooms.sprites()))

    def _handle_room_transition(self, direction):
        # Implement room transition logic here
        # This might involve changing the current room and repositioning the player
        pass

    def draw(self):
        self.game_surface.blit(self.background, (0, 0))
        for room in self.rooms:
            room.draw(self.game_surface)
        self.player.draw(self.game_surface)

        if self.debug_mode:
            # current_room = self._get_current_room()
            # current_room.draw_hitboxes(self.game_surface)
            # self.player_sprite.draw_hitbox(self.game_surface)
            # self.draw_debug_info()
            current_room = next(iter(self.rooms.sprites()))
            # current_room.draw_floor_rect(self.game_surface)
            self.player_sprite.draw_hitbox(self.game_surface)
            self.player_sprite.draw_debug_info(self.game_surface)
            for room in self.rooms:
                room.draw_hitboxes(self.game_surface)
            self.draw_debug_info()

        scaled_surface = pygame.transform.scale(
            self.game_surface, (self.window_width, self.window_height)
        )
        self.screen.blit(scaled_surface, (0, 0))

    def draw_debug_info(self):
        font = pygame.font.Font(None, 20)
        debug_surface = font.render("Debug Mode ON", True, (255, 255, 255))
        self.game_surface.blit(debug_surface, (10, 10))
        print(f"Room position: {self._get_starting_room().rect}")
        print(f"Floor rect: {self._get_starting_room().floor_rect}")
        print(f"Player position: {self.player_sprite.rect}")

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
        clock = pygame.time.Clock()
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    app = Application()
    app.run()

