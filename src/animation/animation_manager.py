from typing import Union, List

import pygame

from src.animation.animation import Animation


class AnimationManager:
    def __init__(self):
        self.animations: dict[str, Animation] = {}
        self.current_animation: Union[Animation, None] = None

    def add_animation(
        self, name: str, frame_paths: List[str], frame_duration: int
    ) -> None:
        self.animations[name] = Animation(name, frame_paths, frame_duration)

    def play(self, name: str) -> None:
        if name in self.animations:
            if self.current_animation != self.animations[name]:
                self.current_animation = self.animations[name]
                self.current_animation.current_frame = 0
                self.current_animation.time_elapsed = 0

    def update(self, dt: int) -> None:
        if self.current_animation:
            self.current_animation.update(dt)

    def get_current_frame(self) -> Union[pygame.Surface, None]:
        if self.current_animation:
            return self.current_animation.get_current_frame()
        return None
