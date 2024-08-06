import sys
import pygame
from src.game.dungeon_adventure import GameModel
from src.dungeon.dungeon_generator import DungeonGenerator
from src.characters.player import Player
from src.enums.room_types import Direction


class Application:
    def __init__(self, width=900, height=750):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dungeon Adventure")

        # Initialize game model
        self.game_model = self.setup_game()

        # Load room images
        self.room_images = {
            "Room 1 - Entrance Hall": pygame.image.load(
                "/Users/saran/DungeonAdventure/src/resources/Room1.png"
            ),
            "Room 2": pygame.image.load(
                "/Users/saran/DungeonAdventure/src/resources/Room2.png"
            ),
            # Need to add more rooms
        }

        # Scale images
        for key in self.room_images:
            self.room_images[key] = pygame.transform.scale(
                self.room_images[key], (self.width, self.height)
            )

    def setup_game(self):
        dungeon = DungeonGenerator.generate_default_dungeon()
        player = Player("Player 1")
        entrance_room = dungeon.get_room("Room 1 - Entrance Hall")
        if entrance_room is None:
            raise ValueError("Dungeon has no entrance room")
        player.current_room = entrance_room
        return GameModel(player, dungeon)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)
        return True

    def handle_key_press(self, key):
        player = self.game_model.player
        current_room = player.current_room
        if key == pygame.K_UP:
            self.move_player(Direction.NORTH)
        elif key == pygame.K_DOWN:
            self.move_player(Direction.SOUTH)
        elif key == pygame.K_LEFT:
            self.move_player(Direction.WEST)
        elif key == pygame.K_RIGHT:
            self.move_player(Direction.EAST)

    def move_player(self, direction):
        player = self.game_model.player
        current_room = player.current_room
        if (
            direction in current_room.connections
            and current_room.connections[direction]
        ):
            player.current_room = current_room.connections[direction]
            print(f"Moved to {player.current_room.name}")
        else:
            print("Cannot move in that direction")

    def draw(self):
        current_room = self.game_model.player.current_room
        if current_room.name in self.room_images:
            self.screen.blit(self.room_images[current_room.name], (0, 0))
        else:
            # Draw a default background if the room image is not found
            self.screen.fill((0, 0, 0))  # Black background

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = Application()
    app.run()
