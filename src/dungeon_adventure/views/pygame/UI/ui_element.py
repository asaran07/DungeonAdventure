from abc import ABC, abstractmethod

import pygame


class UIElement(ABC):
    def __init__(self):
        self.x: int
        self.y: int
        self.width: int
        self.height: int
        self.rect: pygame.Rect
        self.surface: pygame.Surface

    @abstractmethod
    def get_surface(self) -> pygame.Surface:
        pass

    @abstractmethod
    def get_frame(self) -> pygame.Rect:
        pass
