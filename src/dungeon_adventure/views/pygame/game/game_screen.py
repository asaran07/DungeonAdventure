import pygame
from pygame.surface import Surface
from pygame.time import Clock


class GameScreen:
    def __init__(self, width: int = 480, height: int = 270, scale_factor: int = 3):
        """
        Initialize the game screen with given dimensions and scale factor.

        :param width: Base width of the game surface
        :param height: Base height of the game surface
        :param scale_factor: Scale factor for the window size
        """
        pygame.init()
        pygame.display.set_caption("Dungeon Adventure")

        self._width: int = width
        self._height: int = height
        self._scale_factor: int = scale_factor
        self._window_width: int = self._width * self._scale_factor
        self._window_height: int = self._height * self._scale_factor

        self._screen: Surface = pygame.display.set_mode(
            (self._window_width, self._window_height)
        )
        self._game_surface: Surface = Surface((self._width, self._height))
        self._clock: Clock = pygame.time.Clock()

    @property
    def width(self) -> int:
        """Base width of the game surface."""
        return self._width

    @property
    def height(self) -> int:
        """Base height of the game surface."""
        return self._height

    @property
    def scale_factor(self) -> int:
        """Scale factor for the window size."""
        return self._scale_factor

    @property
    def window_width(self) -> int:
        """Width of the game window."""
        return self._window_width

    @property
    def window_height(self) -> int:
        """Height of the game window."""
        return self._window_height

    def get_game_surface(self) -> Surface:
        """Return the base game surface for drawing."""
        return self._game_surface

    def get_screen(self) -> Surface:
        """Return the main screen surface."""
        return self._screen

    def get_scaled_surface(self) -> Surface:
        """Return a scaled version of the game surface to fit the window."""
        return pygame.transform.scale(
            self._game_surface, (self._window_width, self._window_height)
        )

    def tick(self, fps: int) -> float:
        """
        Advance the game clock.

        :param fps: Desired frames per second
        :return: Time elapsed since last frame in seconds
        """
        return self._clock.tick(fps) / 1000.0

    def get_fps(self) -> float:
        """Return the current frames per second."""
        return self._clock.get_fps()

    def flip(self) -> None:
        """Update the full display surface to the screen."""
        pygame.display.flip()

    def clear(self, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        """
        Clear the game surface with a solid color.

        :param color: RGB color tuple to fill the surface with
        """
        self._game_surface.fill(color)

    def blit_scaled(self) -> None:
        """Draw the scaled game surface onto the main screen."""
        self._screen.blit(self.get_scaled_surface(), (0, 0))
