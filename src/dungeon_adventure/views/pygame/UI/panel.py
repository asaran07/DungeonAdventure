from typing import Tuple

import pygame

from dungeon_adventure.views.pygame.UI.ui_element import UIElement


class Panel(UIElement):
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._surface = pygame.Surface(self.size)
        self._frame = pygame.Rect(self.surface.get_rect())

    def create_panel(self, fill_color: Tuple[int, int, int]):
        pygame.draw.rect(self.surface, fill_color, self._frame)

    def add_border(self, border_width: int, border_color: Tuple[int, int, int]):
        pygame.draw.rect(self.surface, border_color, self._frame, border_width)

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def surface(self) -> pygame.Surface:
        return self._surface

    @property
    def frame(self) -> pygame.Rect:
        return self._frame

    def center_of(self, surface: pygame.Surface) -> pygame.Rect:
        return self.surface.get_rect(center=surface.get_rect().center)
