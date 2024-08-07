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
        return [pygame.image.load(path).convert_alpha() for path in frame_paths]

    def update(self, dt: int) -> None:
        if len(self.frames) > 1:  # Only update if there's more than one frame
            self.time_elapsed += dt
            if self.time_elapsed >= self.frame_duration:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.time_elapsed = 0

    def get_current_frame(self) -> pygame.Surface:
        return self.frames[self.current_frame]
