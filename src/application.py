import sys

import pygame

from src.characters.py_player import PyPlayer


def is_running() -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


class Application:
    def __init__(self, width=480, height=270):
        pygame.init()
        self.width = width
        self.height = height
        self.scale_factor = 3
        self.window_width = self.width * self.scale_factor
        self.window_height = self.height * self.scale_factor
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.background = pygame.image.load(
            "/Users/saran/DungeonAdventure/src/resources/default_background.png"
        )
        self.background = pygame.transform.scale(
            self.background, (self.width, self.height)
        )
        self.game_surface = pygame.Surface((self.width, self.height))
        pygame.display.set_caption("Dungeon Adventure")

        self.player = pygame.sprite.GroupSingle()
        self.player_sprite = PyPlayer()
        self.player_sprite.rect.center = (self.width // 2, self.height // 2)
        self.player.add(self.player_sprite)

    def draw(self):
        self.game_surface.blit(self.background, (0, 0))
        self.player.draw(self.game_surface)
        scaled_surface = pygame.transform.scale(
            self.game_surface, (self.window_width, self.window_height)
        )
        self.screen.blit(scaled_surface, (0, 0))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running = is_running()
            self.draw()
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = Application()
    app.run()
