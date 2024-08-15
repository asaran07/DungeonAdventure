import pygame

from dungeon_adventure.views.pygame.UI.ui_element import UIElement


class Panel(UIElement):
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._surface = pygame.Surface((self.width, self.height))
        self._frame = pygame.Rect(self.surface.get_rect())

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
