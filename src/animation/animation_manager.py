from src.animation.animation import Animation


class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.current_animation = None

    def add_animation(self, name, frame_paths, frame_duration):
        self.animations[name] = Animation(name, frame_paths, frame_duration)

    def play(self, name):
        if name in self.animations:
            if self.current_animation != self.animations[name]:
                self.current_animation = self.animations[name]
                self.current_animation.current_frame = 0
                self.current_animation.time_elapsed = 0

    def update(self, dt):
        if self.current_animation:
            self.current_animation.update(dt)

    def get_current_frame(self):
        if self.current_animation:
            return self.current_animation.get_current_frame()
        return None
