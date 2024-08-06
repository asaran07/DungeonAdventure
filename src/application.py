import sys
import pygame

from src.characters.pygame_player import PyPlayer
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

        # Create the player
        self.player = PyPlayer(self.width // 2, self.height // 2)

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
        if key == pygame.K_UP:
            self.move_player(0, -1)
        elif key == pygame.K_DOWN:
            self.move_player(0, 1)
        elif key == pygame.K_LEFT:
            self.move_player(-1, 0)
        elif key == pygame.K_RIGHT:
            self.move_player(1, 0)

    def move_player(self, dx, dy):
        new_x = self.player.rect.x + dx * self.player.speed
        new_y = self.player.rect.y + dy * self.player.speed

        # Check if the new position is within the screen boundaries
        if 0 <= new_x < self.width - self.player.rect.width and 0 <= new_y < self.height - self.player.rect.height:
            self.player.rect.x = new_x
            self.player.rect.y = new_y

    def draw(self):
        current_room = self.game_model.player.current_room
        if current_room.name in self.room_images:
            self.screen.blit(self.room_images[current_room.name], (0, 0))
        else:
            # Draw a default background if the room image is not found
            self.screen.fill((0, 0, 0))  # Black background

        self.player.draw(self.screen)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.player.update()
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = Application()
    app.run()
