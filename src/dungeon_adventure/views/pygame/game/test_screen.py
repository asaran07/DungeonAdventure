import pygame


class TestScreen:
    def __init__(self, width: int, height: int, scale_factor: int):
        self.width = width * scale_factor
        self.height = height * scale_factor
        self.surface: pygame.Surface()
