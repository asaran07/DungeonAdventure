import pygame


class Animation:
    def __init__(self, name, frame_paths, frame_duration):
        self.name = name
        self.frames = self.load_frames(frame_paths)
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_elapsed = 0

    def load_frames(self, frame_paths):
        return [pygame.image.load(path).convert_alpha() for path in frame_paths]

    def update(self, dt):
        if len(self.frames) > 1:  # Only update if there's more than one frame
            self.time_elapsed += dt
            if self.time_elapsed >= self.frame_duration:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.time_elapsed = 0

    def get_current_frame(self):
        return self.frames[self.current_frame]
