import pygame

from dungeon_adventure.config import RESOURCES_DIR


def load_background():
    background = pygame.image.load(
        f"{RESOURCES_DIR}/default_background.png"
    ).convert_alpha()
    return pygame.transform.scale(background, (480, 270))


class ResourceManager:
    def __init__(self):
        self.background = load_background()
