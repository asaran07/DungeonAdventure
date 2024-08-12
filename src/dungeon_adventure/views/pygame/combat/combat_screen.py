import pygame
import pygame.font


class CombatScreen:
    def __init__(self, width, height, scale_factor=3):
        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.font = None
        self.title_font = None
        self.screen = None
        self.initialize()

    def initialize(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 14 * self.scale_factor, bold=True)
        self.title_font = pygame.font.SysFont(None, 16 * self.scale_factor, bold=True)

    def scale(self, value):
        return value * self.scale_factor

    def draw_panel(self, surface, x, y, width, height, bg_color, border_color):
        pygame.draw.rect(surface, bg_color, (self.scale(x), self.scale(y), self.scale(width), self.scale(height)))
        pygame.draw.rect(surface, border_color, (self.scale(x), self.scale(y), self.scale(width), self.scale(height)),
                         self.scale(1))

    def draw_text(self, surface, text, x, y, color, center=False, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (self.scale(x), self.scale(y))
        else:
            text_rect.topleft = (self.scale(x), self.scale(y))
        surface.blit(text_surface, text_rect)

    def draw(self, surface):
        # Main Panel
        self.draw_panel(surface, 45, 25, 390, 219, (120, 81, 79), (94, 58, 56))

        # Text Panel
        self.draw_panel(surface, 72, 37, 339, 85, (217, 217, 217), (0, 0, 0))
        self.draw_text(surface, "sample text", 241, 79, (0, 0, 0), center=True)

        # Attack button
        self.draw_panel(surface, 75, 134, 83, 22, (217, 217, 217), (0, 0, 0))
        self.draw_text(surface, "attack", 116, 145, (0, 0, 0), center=True)

        # Flee button
        self.draw_panel(surface, 75, 167, 83, 21, (217, 217, 217), (0, 0, 0))
        self.draw_text(surface, "flee", 116, 177, (0, 0, 0), center=True)

        # Use Item button
        self.draw_panel(surface, 75, 201, 83, 22, (217, 217, 217), (0, 0, 0))
        self.draw_text(surface, "use item", 116, 212, (0, 0, 0), center=True)

        # HP Panel
        self.draw_panel(surface, 182, 134, 109, 89, (217, 217, 217), (0, 0, 0))
        self.draw_text(surface, "HP", 236, 144, (0, 0, 0), center=True, font=self.title_font)

        # HP Display Bar
        self.draw_panel(surface, 199, 163, 75, 16, (199, 44, 44), (0, 0, 0))

        # Empty Panel
        self.draw_panel(surface, 303, 134, 108, 89, (217, 217, 217), (0, 0, 0))

    def update(self, dt):
        # Add any combat screen-specific updates here
        pass

    def handle_event(self, event):
        # Add event handling for combat screen interactions
        pass