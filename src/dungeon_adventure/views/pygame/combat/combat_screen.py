import logging

import pygame

from dungeon_adventure.views.pygame.game.game_screen import GameScreen

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class CombatScreen:
    def __init__(self, window_width: int, window_height: int):
        self._width = window_width
        self._height = window_height
        self._display = pygame.Surface((self._width - 50, self._height - 50))
        self.logger = logging.getLogger(__name__)

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, surface: pygame.Surface):
        self._display = surface

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def draw(self, screen: pygame.Surface):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, WHITE, self.display.get_rect(), 2)
        centering_rect = screen.get_rect()
        display_rect = self.display.get_rect(center=centering_rect.center)

        title_surface = pygame.font.Font(None, 48).render("BATTLE", True, WHITE)
        title_rect = title_surface.get_rect(center=self.display.get_rect().center)

        self.display.blit(title_surface, title_rect)

        screen.blit(self.display, display_rect)
