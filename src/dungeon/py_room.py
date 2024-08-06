import pygame


class PyRoom(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        floor_left = (128 - 96) // 2  # Centering the floor horizontally
        floor_top = (80 - 48) // 2  # Centering the floor vertically
        self._floor_rect = pygame.Rect(floor_left, floor_top, 96, 48)

    @property
    def floor_rect(self):
        # Return the floor rect adjusted for the room's position on the game surface
        x = (480 - 128) // 2
        y = (270 - 80) // 2
        return self._floor_rect.move(x, y)

    def is_within_floor(self, rect) -> bool:
        return self.floor_rect.contains(rect)

    def draw_floor_rect(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), self.floor_rect, 2)  # Blue rectangle
