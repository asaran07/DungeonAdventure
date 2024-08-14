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
        self.font = None
        self.message = ""

    def set_message(self, message: str):
        self.message = message

    def _ensure_font_initialized(self):
        if self.font is None:
            if not pygame.font.get_init():
                pygame.font.init()
            self.font = pygame.font.Font(None, 30)

    # def get_current_message(self):
    #     # if self.current_room is None:
    #     #     return "Initializing game..."
    #     if self.current_room.room.room_type is RoomType.PIT:
    #         return "Oh no! This room has a spike trap! You've taken damage."
    #     else:
    #         return "Is there even anything in this room?"

    def draw(self, surface: pygame.Surface):
        # Draw background
        pygame.draw.rect(surface, (50, 50, 50), self.controls_rect)
        pygame.draw.rect(surface, (200, 200, 200), self.controls_rect, 2)

        self._ensure_font_initialized()

        if hasattr(self, "message"):
            text_surface = self.font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.controls_rect.center)
            surface.blit(text_surface, text_rect)
