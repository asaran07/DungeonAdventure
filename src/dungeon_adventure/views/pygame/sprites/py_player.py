import os

import pygame

from dungeon_adventure.config import RESOURCES_DIR
from dungeon_adventure.views.pygame.animation.animation_manager import AnimationManager


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
        # TODO: Extract this animation functionality into its own class.

        base_path = os.path.join(RESOURCES_DIR, 'hero_animations', 'hero_walk')

        # Load idle animation (single frame)
        idle_path = os.path.join(base_path, "hero_idle.png")

        # We can just use the hero_idle image for both idling left and right for now
        self.animation_manager.add_animation("idle_right", [idle_path], 1000)
        self.animation_manager.add_animation("idle_left", [idle_path], 1000)

        # Create a list of all the 'hero_walk' animation types by adding the 'i' value right after 'hero_walk_'
        # This way we get the ../hero_walk_1, ../hero_walk_2 etc
        walk_paths = [
            os.path.join(base_path, f"hero_walk_{i}.png") for i in range(1, 8)
        ]

        # Then we add all those in the animation manager
        self.animation_manager.add_animation(
            "walk_right", walk_paths, 1000 // 12
        )  # 12 fps

        # We do the same for walk left, but we use the same assets because we can just flip the walk_right images.
        self.animation_manager.add_animation("walk_left", walk_paths, 1000 // 12)

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
        dx = (
            (keys[pygame.K_RIGHT] or keys[pygame.K_d])
            - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        ) * self.speed
        dy = (
            (keys[pygame.K_DOWN] or keys[pygame.K_s])
            - (keys[pygame.K_UP] or keys[pygame.K_w])
        ) * self.speed

        # Then depending on which way we're facing, we play that certain animation group
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

    def draw_debug_info(self, surface: pygame.Surface) -> None:
        font = pygame.font.Font(None, 14)
        current_animation = self.animation_manager.current_animation
        if current_animation:
            debug_text = (
                f"Animation: {current_animation.name}, Frame: {current_animation.current_frame + 1}/"
                f"{len(current_animation.frames)}"
            )
            debug_surface = font.render(debug_text, True, (255, 255, 255))
            surface.blit(debug_surface, (self.rect.x, self.rect.y - 30))
