import pygame


class PlayerMessageDisplay:
    def __init__(self, screen_width: int, screen_height: int):
        self.controls_width = int(screen_width * 0.90)  # 90% of screen width
        self.controls_height = int(screen_height * 0.15)  # 15% of screen height
        self.controls_rect = pygame.Rect(
            screen_width - self.controls_width - 70,
            screen_height - self.controls_height - 10,
            self.controls_width,
            self.controls_height,
        )
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface: pygame.Surface):
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), self.controls_rect)
        pygame.draw.rect(surface, (200, 200, 200), self.controls_rect, 2)