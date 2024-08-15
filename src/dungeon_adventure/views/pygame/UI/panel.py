from typing import Tuple

import pygame

from dungeon_adventure.views.pygame.UI.ui_element import UIElement


class Panel(UIElement):
    BEIGE = (120, 81, 79)
    DARK_BROWN = (94, 58, 56)
    OFF_WHITE = (217, 217, 217)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._surface = pygame.Surface(self.size)
        self._frame = pygame.Rect(self.surface.get_rect())

    def add_text(self, text: str):
        text_surface = pygame.font.SysFont(None, 24).render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text_surface, text_rect)

    def create_default_panel(self):
        self.create_panel(self.OFF_WHITE)
        self.add_border(2, self.BLACK)

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

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    def center_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(center=target_rect.center)

    def top_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(midtop=target_rect.midtop)

    def bottom_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(midbottom=target_rect.midbottom)

    def left_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(midleft=target_rect.midleft)

    def right_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(midright=target_rect.midright)

    def top_left_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(topleft=target_rect.topleft)

    def top_right_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(topright=target_rect.topright)

    def bottom_left_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(bottomleft=target_rect.bottomleft)

    def bottom_right_of(self, surface: pygame.Surface, padding: int = 0) -> pygame.Rect:
        target_rect = surface.get_rect().inflate(-padding * 2, -padding * 2)
        return self.surface.get_rect(bottomright=target_rect.bottomright)

    def align(
        self, surface: pygame.Surface, position: str, padding: int = 0
    ) -> pygame.Rect:
        position = position.lower()
        if position == "center":
            return self.center_of(surface, padding)
        elif position == "top":
            return self.top_of(surface, padding)
        elif position == "bottom":
            return self.bottom_of(surface, padding)
        elif position == "left":
            return self.left_of(surface, padding)
        elif position == "right":
            return self.right_of(surface, padding)
        elif position == "top_left":
            return self.top_left_of(surface, padding)
        elif position == "top_right":
            return self.top_right_of(surface, padding)
        elif position == "bottom_left":
            return self.bottom_left_of(surface, padding)
        elif position == "bottom_right":
            return self.bottom_right_of(surface, padding)
        else:
            raise ValueError(f"Invalid position: {position}")
