from abc import ABC, abstractmethod
import pygame


class UIElement(ABC):
    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass

    @property
    @abstractmethod
    def surface(self) -> pygame.Surface:
        pass

    @property
    @abstractmethod
    def frame(self) -> pygame.Rect:
        pass

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height
