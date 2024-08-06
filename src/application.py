import sys
import pygame
from pygame import Surface

from src.characters.pygame_player import PyPlayer
from src.game.dungeon_adventure import GameModel
from src.dungeon.dungeon_generator import DungeonGenerator
from src.characters.player import Player
from src.enums.room_types import Direction


class Application:
    def __init__(self, width=480, height=270):
        pygame.init()
        self.width = width
        self.height = height
        self.scale_factor = 3
        self.window_width = self.width * self.scale_factor
        self.window_height = self.height * self.scale_factor

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.background = pygame.image.load("/Users/saran/DungeonAdventure/src/resources/default_background.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.game_surface = pygame.Surface((self.width, self.height))

        pygame.display.set_caption("Dungeon Adventure")

    def is_runnign(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        # Draw the background onto the game surface
        self.game_surface.blit(self.background, (0, 0))

        # Scale the game surface up to the window size
        scaled_surface = pygame.transform.scale(self.game_surface, (self.window_width, self.window_height))
        self.screen.blit(scaled_surface, (0, 0))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running = self.is_runnign()
            self.draw()
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = Application()
    app.run()
