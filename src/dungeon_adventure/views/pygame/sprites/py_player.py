import pygame
import os
from dungeon_adventure.config import RESOURCES_DIR
from dungeon_adventure.views.pygame.animation.animation_manager import AnimationManager
from dungeon_adventure.views.pygame.room.game_room import GameRoom


class PyPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animation_manager = AnimationManager()
        self.image = None
        self.rect = None
        self.speed = 2
        self.foot_height = 5
        self.facing_right = True

    def initialize(self):
        self.load_animations()
        self.animation_manager.play("idle_right")
        self.image = self.animation_manager.get_current_frame().convert_alpha()
        if self.image is None:
            raise ValueError("Player image is None. Check animation loading.")
        self.rect = self.image.get_rect()

    def load_animations(self):
        base_path = os.path.join(RESOURCES_DIR, "hero_animations", "hero_walk")
        idle_path = os.path.join(base_path, "hero_idle.png")

        # Load idle animations
        self.animation_manager.add_animation("idle_right", [idle_path], 1000)
        self.animation_manager.add_animation("idle_left", [idle_path], 1000)

        # Load walk animations
        walk_paths = [
            os.path.join(base_path, f"hero_walk_{i}.png") for i in range(1, 8)
        ]
        self.animation_manager.add_animation("walk_right", walk_paths, 1000 // 12)
        self.animation_manager.add_animation("walk_left", walk_paths, 1000 // 12)

    def update(self, dt, current_room: GameRoom):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (
            keys[pygame.K_UP] or keys[pygame.K_w]
        )

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

        self.move(dx * self.speed, dy * self.speed, current_room)
        self.animation_manager.update(dt)

        self.image = self.animation_manager.get_current_frame()
        if self.image is None:
            raise ValueError(
                "Player image is None after update. Check animation update logic."
            )
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        # Ensure rect is always updated
        if self.rect is None:
            self.rect = self.image.get_rect()
        else:
            new_rect = self.image.get_rect()
            self.rect.size = new_rect.size

    def move(self, dx, dy, current_room: GameRoom):
        if self.rect is None:
            self.rect = self.image.get_rect()

        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Check if the new position is within the floor area
        feet_position = (
            new_x + self.rect.width // 2,
            new_y + self.rect.height - self.foot_height // 2,
        )
        can_move = current_room.is_within_floor(feet_position)

        # print(f"Attempting to move to {feet_position}. Can move: {can_move}")

        if can_move:
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            # If not, try to move in x and y directions separately
            can_move_x = current_room.is_within_floor(
                (new_x + self.rect.width // 2, self.rect.centery)
            )
            can_move_y = current_room.is_within_floor(
                (self.rect.centerx, new_y + self.rect.height - self.foot_height // 2)
            )

            # print(f"Can move X: {can_move_x}, Can move Y: {can_move_y}")

            if can_move_x:
                self.rect.x = new_x
            if can_move_y:
                self.rect.y = new_y

    def draw_hitbox(self, surface):
        if self.rect is not None:
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
            feet_y = self.rect.bottom - self.foot_height
            pygame.draw.line(
                surface,
                (0, 255, 0),
                (self.rect.left, feet_y),
                (self.rect.right, feet_y),
                1,
            )

    def draw_debug_info(self, surface: pygame.Surface) -> None:
        if self.rect is not None:
            font = pygame.font.Font(None, 14)
            current_animation = self.animation_manager.current_animation
            if current_animation:
                debug_text = (
                    f"Animation: {current_animation.name}, Frame: {current_animation.current_frame + 1}/"
                    f"{len(current_animation.frames)}"
                )
                debug_surface = font.render(debug_text, True, (255, 255, 255))
                surface.blit(debug_surface, (self.rect.x, self.rect.y - 30))
