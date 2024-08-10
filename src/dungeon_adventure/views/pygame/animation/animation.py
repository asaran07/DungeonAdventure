from typing import List

import pygame


class Animation:
    def __init__(self, name: str, frame_paths: List[str], frame_duration: int):
        self.name: str = name
        self.frames: List[pygame.Surface] = self.load_frames(frame_paths)
        self.frame_duration: int = frame_duration
        self.current_frame: int = 0
        self.time_elapsed: int = 0

    def load_frames(self, frame_paths: List[str]) -> List[pygame.Surface]:
        # So this basically takes the paths we specified, and then gets those
        # images and loads them into a list as the pygame's Surface property.
        # So we get a bunch of surfaces derived from files back.
        # We can then load the surfaces into our 'frames' list.
        return [pygame.image.load(path).convert_alpha() for path in frame_paths]

    def update(self, dt: int) -> None:
        if len(self.frames) > 1:  # Only update if there's at least one frame,
            # (so we don't update if we have a single image for idle properties).
            self.time_elapsed += dt
            # Then we switch to the next frame after we get to our frame duration delay amount
            if self.time_elapsed >= self.frame_duration:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                # Reset the time_elapsed variable for the next frame
                self.time_elapsed = 0

    def get_current_frame(self) -> pygame.Surface:
        # A frame is basically just a surface maybe I should rename that for clarity
        return self.frames[self.current_frame]
