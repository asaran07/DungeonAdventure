import logging
from typing import Optional

import pygame

from dungeon_adventure.logging_config import setup_logging
from dungeon_adventure.views.pygame.UI.panel import Panel


class TestScreen:
    BEIGE = (120, 81, 79)
    DARK_BROWN = (94, 58, 56)
    OFF_WHITE = (217, 217, 217)
    BLACK = (0, 0, 0)

    def __init__(self, width: int, height: int, scale_factor: int):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.width = width * scale_factor * 0.9
        self.height = height * scale_factor * 0.9
        self.surface: pygame.Surface = pygame.Surface(self.size)
        self._screen: Optional[pygame.Surface] = None
        self.main_panel = Panel(*self.surface.size)
        self.panels: [pygame.Surface] = []

    @property
    def screen(self) -> pygame.Surface:
        """The screen to draw on."""
        return self._screen

    @screen.setter
    def screen(self, screen: pygame.Surface):
        self._screen = screen

    @property
    def size(self):
        return self.width, self.height

    def draw(self):
        self.check_null_screen()
        self.main_panel.create_panel(self.BEIGE)
        self.main_panel.add_border(10, self.DARK_BROWN)
        self.surface.blit(
            self.main_panel.surface,
            self.main_panel.center_of(self.surface),
        )

        panel = Panel(self.main_panel.width - 65, self.main_panel.height // 2)
        panel.create_default_panel()
        panel.add_text("This is some testing text.", 24, self.BLACK, "top_right")

        self.surface.blit(panel.surface, panel.align(self.surface, "top", 30))
        self.screen.blit(self.surface, self.center)

    @property
    def center(self) -> Optional[pygame.Rect]:
        self.check_null_screen()
        return self.surface.get_rect(center=self.screen.get_rect().center)

    def check_null_screen(self):
        if self._screen is None:
            raise ValueError("No surface set for drawing. Call set_surface() first.")


if __name__ == "__main__":
    setup_logging()
    pygame.init()
    screen_width, screen_height = 480, 270
    pygame_screen = pygame.display.set_mode((screen_width * 3, screen_height * 3))
    pygame.display.set_caption("UI Test")

    ui_screen = TestScreen(480, 270, 3)  # Instantiate your Screen class
    ui_screen.screen = pygame_screen

    # Add some UI elements to your screen for testing
    # For example:
    # ui_screen.add_panel(x=100, y=100, width=200, height=150)
    # ui_screen.add_button(x=150, y=200, width=100, height=50, text="Test Button")

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle other events if needed
            # ui_screen.handle_event(event)

        pygame_screen.fill((255, 255, 255))  # Fill with white background

        # Draw your UI elements
        ui_screen.draw()

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
