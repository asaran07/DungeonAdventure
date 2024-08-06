import pygame


class PyPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            "/Users/saran/DungeonAdventure/src/resources/default_hero_small.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 2

    def move(self, dx, dy, floor_rect):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        new_x = max(floor_rect.left, min(new_x, floor_rect.right - self.rect.width))
        new_y = max(floor_rect.top, min(new_y, floor_rect.bottom - self.rect.height))
        self.rect.x = new_x
        self.rect.y = new_y

    def update(self, floor_rect):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        self.move(dx, dy, floor_rect)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)  # Red rectangle
