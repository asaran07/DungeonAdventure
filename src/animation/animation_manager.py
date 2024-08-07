from typing import Union, List

import pygame

from src.animation.animation import Animation


class AnimationManager:
    def __init__(self):
        # We assign a name to a sequence of pygame 'Surfaces', aka our custom Animation class, so that we can
        # call or/play them according to what animation need to display.
        # This hiarky is needed cause if we have unique animations for different actions like walking left or walking
        # right or jumping or idling etc., we must be able to play that specific batch/sequence/set of animations.
        self.animations: dict[str, Animation] = {}
        # There's probably a better way to write this, this seems kinda smelly lol
        self.current_animation: Union[Animation, None] = None

    def add_animation(
        self, name: str, frame_paths: List[str], frame_duration: int
    ) -> None:
        self.animations[name] = Animation(name, frame_paths, frame_duration)

    def play(self, name: str) -> None:
        # If the requested animation is in our list of animations
        if name in self.animations:
            # and if the requested current animation isn't the same as the one currently selected
            if self.current_animation != self.animations[name]:
                # then we set the current animation to the requested animation.
                self.current_animation = self.animations[name]
                self.current_animation.current_frame = 0
                self.current_animation.time_elapsed = 0

    # This method is here so that when we updated our animations along with pygame's clock, so as time progresses,
    # we cycle through our animation sequences concurrently and sequentially.
    def update(self, dt: int) -> None:
        if self.current_animation:
            self.current_animation.update(dt)

    def get_current_frame(self) -> Union[pygame.Surface, None]:
        if self.current_animation:
            return self.current_animation.get_current_frame()
        return None
