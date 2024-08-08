import pygame

class ControlsDisplay:

    def __init__(self, screen_width: int, screen_height: int, scale_factor: int):
        self.scale_factor = scale_factor
        self.controls_width = 80 * scale_factor
        self.controls_height = 50 * scale_factor
        self.controls_rect = pygame.Rect(
            (screen_width - self.controls_width) - (5 * scale_factor),
            (screen_height - self.controls_height) - (130 * scale_factor),
            self.controls_width,
            self.controls_height
            )
        self.font = pygame.font.Font(None, 8 * scale_factor)
        self.keybinds = [
            ("WASD", "Movement"),
            ("T", "Take Items"),
            ("X", "Drop Items"),
            ("B", "Debug"),
        ]

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (50, 50, 50), self.controls_rect)
        pygame.draw.rect(surface, (200, 200, 200), self.controls_rect, 2)

        title_surface = self.font.render("Controls", False, (255, 255, 255))

        surface.blit(title_surface, (self.controls_rect.x + (5 * self.scale_factor), self.controls_rect.y + (5 * self.scale_factor)))

        for i, (key, value) in enumerate(self.keybinds):
            key_surface = self.font.render(key, False, (255, 255, 255))
            value_surface = self.font.render(value, False, (255, 255, 255))
            y_pos = self.controls_rect.y + ((i + 2) * 8 * self.scale_factor)
            surface.blit(key_surface, (self.controls_rect.x + (10 * self.scale_factor), y_pos))
            surface.blit(value_surface, (self.controls_rect.x + (40 * self.scale_factor), y_pos))


