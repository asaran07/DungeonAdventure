import os

import pygame

from src.animation.animation_manager import AnimationManager


class PyPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_manager = AnimationManager()
        self.load_animations()
        self.animation_manager.play("idle_right")
        self.image = self.animation_manager.get_current_frame()
        self.rect = self.image.get_rect()
        self.speed = 2
        self.foot_height = 5
        self.facing_right = True

    def load_animations(self):
        base_path = (
            "/Users/saran/DungeonAdventure/src/resources/hero_animations/hero_walk/"
        )

        # Load idle animation (single frame)
        idle_path = os.path.join(base_path, "hero_idle.png")
        self.animation_manager.add_animation("idle_right", [idle_path], 1000)

        # For idle_left we flip the image live
        self.animation_manager.add_animation("idle_left", [idle_path], 1000)

        # Load walking animation
        walk_paths = [
            os.path.join(base_path, f"hero_walk_{i}.png") for i in range(1, 8)
        ]
        self.animation_manager.add_animation(
            "walk_right", walk_paths, 1000 / 12
        )  # 12 fps

        # We flip the images live for walk_left as well
        self.animation_manager.add_animation("walk_left", walk_paths, 1000 / 12)

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

    def update(self, dt, floor_rect):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed

        if dx > 0:
            self.animation_manager.play("walk_right")
            self.facing_right = True
        elif dx < 0:
            self.animation_manager.play("walk_left")
            self.facing_right = False
        elif dy != 0:
            self.animation_manager.play(
                "walk_right" if self.facing_right else "walk_left"
            )
        else:
            self.animation_manager.play(
                "idle_right" if self.facing_right else "idle_left"
            )

        self.move(dx, dy, floor_rect)
        self.animation_manager.update(dt)

        # Get the current frame and flip it if facing left
        self.image = self.animation_manager.get_current_frame()
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)  # Red rectangle
        # Draw a green line at the "feet" level
        feet_y = self.rect.bottom - self.foot_height
        pygame.draw.line(
            surface, (0, 255, 0), (self.rect.left, feet_y), (self.rect.right, feet_y), 2
        )
