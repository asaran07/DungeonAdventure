from typing import Tuple

import pygame

from dungeon_adventure.views.pygame.UI.ui_element import UIElement


class Bar(UIElement):
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._surface = pygame.Surface((width, height))
        self._frame = self._surface.get_rect()

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

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height
