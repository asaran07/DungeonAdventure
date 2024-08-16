from typing import Optional, Tuple

import pygame
from pygame import Font, Surface
from pygame.font import SysFont

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

    def add_text(
        self,
        text: str,
        size: int,
        color: Tuple[int, int, int],
        position: str = "center",
        padding: int = 0,
        font_name: Optional[str] = None,
        antialiasing: bool = True,
    ):
        font = (
            pygame.font.SysFont(font_name, size)
            if font_name
            else pygame.font.Font(None, size)
        )
        text_surface = font.render(text, antialiasing, color)
        text_rect = text_surface.get_rect()

        panel_rect = self.surface.get_rect().inflate(-padding * 2, -padding * 2)

        if position == "center":
            text_rect.center = panel_rect.center
        elif position == "top":
            text_rect.midtop = panel_rect.midtop
        elif position == "bottom":
            text_rect.midbottom = panel_rect.midbottom
        elif position == "left":
            text_rect.midleft = panel_rect.midleft
        elif position == "right":
            text_rect.midright = panel_rect.midright
        elif position == "topleft":
            text_rect.topleft = panel_rect.topleft
        elif position == "topright":
            text_rect.topright = panel_rect.topright
        elif position == "bottomleft":
            text_rect.bottomleft = panel_rect.bottomleft
        elif position == "bottomright":
            text_rect.bottomright = panel_rect.bottomright
        else:
            raise ValueError(f"Invalid position: {position}")

        self.surface.blit(text_surface, text_rect)

    def add_multiline_text(
        self,
        text: str,
        size: int,
        color: Tuple[int, int, int],
        position: str = "center",
        padding: int = 0,
        line_spacing: int = 5,
        font_name: Optional[str] = None,
        antialiasing: bool = True,
        align: str = "left",
    ):
        font = (
            pygame.font.SysFont(font_name, size)
            if font_name
            else pygame.font.Font(None, size)
        )
        lines = text.split("\n")
        text_surfaces = [font.render(line, antialiasing, color) for line in lines]

        total_height = sum(
            surface.get_height() for surface in text_surfaces
        ) + line_spacing * (len(lines) - 1)
        max_width = max(surface.get_width() for surface in text_surfaces)

        text_area = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        y_offset = 0

        for surface in text_surfaces:
            if align == "left":
                x_offset = 0
            elif align == "center":
                x_offset = (max_width - surface.get_width()) // 2
            elif align == "right":
                x_offset = max_width - surface.get_width()
            else:
                raise ValueError(f"Invalid alignment: {align}")

            text_area.blit(surface, (x_offset, y_offset))
            y_offset += surface.get_height() + line_spacing

        text_rect = text_area.get_rect()
        panel_rect = self.surface.get_rect().inflate(-padding * 2, -padding * 2)

        if position == "center":
            text_rect.center = panel_rect.center
        elif position == "top":
            text_rect.midtop = panel_rect.midtop
        elif position == "bottom":
            text_rect.midbottom = panel_rect.midbottom
        elif position == "left":
            text_rect.midleft = panel_rect.midleft
        elif position == "right":
            text_rect.midright = panel_rect.midright
        elif position == "topleft":
            text_rect.topleft = panel_rect.topleft
        elif position == "topright":
            text_rect.topright = panel_rect.topright
        elif position == "bottomleft":
            text_rect.bottomleft = panel_rect.bottomleft
        elif position == "bottomright":
            text_rect.bottomright = panel_rect.bottomright
        else:
            raise ValueError(f"Invalid position: {position}")

        self.surface.blit(text_area, text_rect)

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
