import pygame
import pygame.font
from enum import Enum, auto


class CombatAction(Enum):
    ATTACK = auto()
    FLEE = auto()
    USE_ITEM = auto()


class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False

    def draw(self, surface, font, scale_factor):
        color = (180, 180, 180) if self.hovered else (217, 217, 217)
        scaled_rect = pygame.Rect(
            self.rect.x * scale_factor,
            self.rect.y * scale_factor,
            self.rect.width * scale_factor,
            self.rect.height * scale_factor,
        )
        pygame.draw.rect(surface, color, scaled_rect)
        pygame.draw.rect(surface, (0, 0, 0), scaled_rect, scale_factor)

        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event, scale_factor):
        scaled_rect = pygame.Rect(
            self.rect.x * scale_factor,
            self.rect.y * scale_factor,
            self.rect.width * scale_factor,
            self.rect.height * scale_factor,
        )
        if event.type == pygame.MOUSEMOTION:
            self.hovered = scaled_rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if scaled_rect.collidepoint(event.pos):
                return self.action
        return None


class CombatScreen:
    def __init__(self, width, height, scale_factor=3):
        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.font = None
        self.title_font = None
        self.buttons = []
        self.message = "Combat started!"
        self.player_hp = 100
        self.player_max_hp = 100
        self.initialize()

    def initialize(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 14 * self.scale_factor, bold=True)
        self.title_font = pygame.font.SysFont(None, 16 * self.scale_factor, bold=True)
        self.buttons = [
            Button(75, 134, 83, 22, "attack", CombatAction.ATTACK),
            Button(75, 167, 83, 21, "flee", CombatAction.FLEE),
            Button(75, 201, 83, 22, "use item", CombatAction.USE_ITEM),
        ]

    def scale(self, value):
        return value * self.scale_factor

    def draw_panel(self, surface, x, y, width, height, bg_color, border_color):
        pygame.draw.rect(
            surface,
            bg_color,
            (self.scale(x), self.scale(y), self.scale(width), self.scale(height)),
        )
        pygame.draw.rect(
            surface,
            border_color,
            (self.scale(x), self.scale(y), self.scale(width), self.scale(height)),
            self.scale(1),
        )

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
        self.draw_text(surface, self.message, 241, 79, (0, 0, 0), center=True)

        # Buttons
        for button in self.buttons:
            button.draw(surface, self.font, self.scale_factor)

        # HP Panel
        self.draw_panel(surface, 182, 134, 109, 89, (217, 217, 217), (0, 0, 0))
        self.draw_text(
            surface, "HP", 236, 144, (0, 0, 0), center=True, font=self.title_font
        )

        # HP Display Bar
        hp_percentage = self.player_hp / self.player_max_hp
        hp_width = int(75 * hp_percentage)
        self.draw_panel(surface, 199, 163, hp_width, 16, (199, 44, 44), (0, 0, 0))
        self.draw_panel(
            surface, 199 + hp_width, 163, 75 - hp_width, 16, (150, 150, 150), (0, 0, 0)
        )
        hp_text = f"{self.player_hp}/{self.player_max_hp}"
        self.draw_text(surface, hp_text, 236, 171, (0, 0, 0), center=True)

        # Empty Panel
        self.draw_panel(surface, 303, 134, 108, 89, (217, 217, 217), (0, 0, 0))

    def update(self, dt):
        # Add any time-based updates here
        pass

    def handle_event(self, event):
        for button in self.buttons:
            action = button.handle_event(event, self.scale_factor)
            if action:
                return action
        return None

    def set_message(self, message):
        self.message = message

    def update_player_hp(self, current_hp, max_hp):
        self.player_hp = current_hp
        self.player_max_hp = max_hp


# Example usage:
if __name__ == "__main__":
    pygame.init()
    width, height = 480, 270
    scale_factor = 3
    screen = pygame.display.set_mode((width * scale_factor, height * scale_factor))
    pygame.display.set_caption("Combat Screen")

    combat_screen = CombatScreen(width, height, scale_factor)

    running = True
    clock = pygame.time.Clock()
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            action = combat_screen.handle_event(event)
            if action:
                print(f"Action triggered: {action}")
                combat_screen.set_message(f"{action} action performed!")

        combat_screen.update(dt)

        screen.fill((255, 255, 255))  # White background
        combat_screen.draw(screen)
        pygame.display.flip()

    pygame.quit()
