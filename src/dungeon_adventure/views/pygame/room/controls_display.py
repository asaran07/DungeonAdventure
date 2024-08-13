import pygame


class ControlsDisplay:
    def __init__(self, screen_width: int, screen_height: int):
        self.controls_width = int(screen_width * 0.15)  # 15% of screen width
        self.controls_height = int(screen_height * 0.25)  # 25% of screen height
        self.controls_rect = pygame.Rect(
            screen_width - self.controls_width - 10,
            screen_height - self.controls_height - 315,
            self.controls_width,
            self.controls_height,
        )
        self.font = pygame.font.Font(None, 24)
        self.keybindings = [
            ("WASD", "Movement"),
            ("I", "Inventory"),
            ("M", "Map"),
            ("T", "Take Items"),
            ("X", "Drop Items"),
            # ("B", "Debug"),
        ]

    def draw(self, surface: pygame.Surface):
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), self.controls_rect)
        pygame.draw.rect(surface, (200, 200, 200), self.controls_rect, 2)

        # Draw title
        title_surface = self.font.render("Controls", True, (255, 255, 255))
        surface.blit(
            title_surface, (self.controls_rect.x + 70, self.controls_rect.y + 10)
        )

        # Draw keybindings
        for i, (key, value) in enumerate(self.keybindings):
            key_surface = self.font.render(key, True, (255, 255, 255))
            value_surface = self.font.render(value, True, (255, 255, 255))
            y_pos = self.controls_rect.y + 50 + i * 30
            surface.blit(key_surface, (self.controls_rect.x + 20, y_pos))
            surface.blit(value_surface, (self.controls_rect.x + 100, y_pos))
