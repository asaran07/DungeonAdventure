import pygame


class PyPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            "/Users/saran/DungeonAdventure/src/resources/default_hero.png"
        )
        self.rect = self.image.get_rect()
