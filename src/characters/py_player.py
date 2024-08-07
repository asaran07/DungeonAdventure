import pygame


class PyPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            "/Users/saran/DungeonAdventure/src/resources/default_hero_small.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = 2
        self.foot_height = 5

    def move(self, dx, dy, floor_rect):
        # Calculate new position
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Create a temporary rect for collision checking
        temp_rect = self.rect.copy()
        temp_rect.x = new_x
        temp_rect.y = new_y

        # Constrain horizontally
        if temp_rect.left < floor_rect.left:
            new_x = floor_rect.left
        elif temp_rect.right > floor_rect.right:
            new_x = floor_rect.right - self.rect.width

        # Constrain vertically, using an adjusted point for top collision
        if temp_rect.bottom > floor_rect.bottom:
            new_y = floor_rect.bottom - self.rect.height
        elif temp_rect.bottom - self.foot_height < floor_rect.top:
            new_y = floor_rect.top - self.rect.height + self.foot_height

        # Update position
        self.rect.x = new_x
        self.rect.y = new_y

    def update(self, floor_rect):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        self.move(dx, dy, floor_rect)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)  # Red rectangle
        # Draw a green line at the "feet" level
        feet_y = self.rect.bottom - self.foot_height
        pygame.draw.line(surface, (0, 255, 0), (self.rect.left, feet_y), (self.rect.right, feet_y), 2)
