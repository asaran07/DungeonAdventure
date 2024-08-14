import pygame


class PlayerStatusDisplay:
    def __init__(self, screen_width: int, screen_height: int, scale_factor: int = 3):
        self.scale_factor = scale_factor
        self.display_rect = pygame.Rect(
            10 * scale_factor,
            10 * scale_factor,
            100 * scale_factor,
            50 * scale_factor
        )
        self.colors = {
            "background": (50, 50, 50, 200),  # Semi-transparent dark gray
            "border": (200, 200, 200),  # Light gray
            "text": (255, 255, 255),  # White
            "hp_bar": (199, 44, 44)  # Red for HP bar
        }
        self.fonts = {
            "status": pygame.font.Font(None, 16 * scale_factor),
            "hp": pygame.font.Font(None, 14 * scale_factor)
        }

    def draw(self, surface: pygame.Surface, player):
        # Draw background
        pygame.draw.rect(surface, self.colors["background"], self.display_rect)
        pygame.draw.rect(surface, self.colors["border"], self.display_rect, 2)

        # Draw player name and status
        name_surface = self.fonts["status"].render(player.name, True, self.colors["text"])
        surface.blit(name_surface, (self.display_rect.x + 10, self.display_rect.y + 10))

        # Draw HP bar
        hp_ratio = player.hero.current_hp / player.hero.max_hp
        hp_bar_width = (self.display_rect.width - 20) * hp_ratio
        hp_bar_rect = pygame.Rect(
            self.display_rect.x + 10,
            self.display_rect.y + 110,
            hp_bar_width,
            20
        )
        pygame.draw.rect(surface, self.colors["hp_bar"], hp_bar_rect)

        # Draw HP text
        hp_text = f"HP: {player.hero.current_hp}/{player.hero.max_hp}"
        hp_surface = self.fonts["hp"].render(hp_text, True, self.colors["text"])
        hp_text_pos = (self.display_rect.x + 15, self.display_rect.y + 80)
        surface.blit(hp_surface, hp_text_pos)

    def update(self, player):
        pass
