import logging
from typing import Callable

import pygame
import pygame.font
from enum import Enum, auto


class CombatAction(Enum):
    ATTACK = auto()
    FLEE = auto()
    USE_ITEM = auto()
    TEST = auto()


class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.blink_state = False

    def draw(self, surface, font, scale_factor):
        color = (180, 180, 180) if self.hovered else (217, 217, 217)
        if self.blink_state:
            color = (255, 255, 0)  # Yellow for blinking
        scaled_rect = pygame.Rect(
            self.rect.x * scale_factor,
            self.rect.y * scale_factor,
            self.rect.width * scale_factor,
            self.rect.height * scale_factor,
        )
        pygame.draw.rect(surface, color, scaled_rect)
        pygame.draw.rect(surface, (0, 0, 0), scaled_rect, scale_factor)

        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event, scale_factor):
        scaled_rect = pygame.Rect(
            self.rect.x * scale_factor,
            self.rect.y * scale_factor,
            self.rect.width * scale_factor,
            self.rect.height * scale_factor,
        )
        if event.type == pygame.MOUSEMOTION:
            self.hovered = scaled_rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if scaled_rect.collidepoint(event.pos):
                return self.action
        return None


class AnimationEvent:
    def __init__(self, delay, action, *args):
        self.delay = delay
        self.action = action
        self.args = args


class CombatScreen:
    def __init__(self, width, height, scale_factor=3):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.elapsed_log_time = 0
        self.log_interval = 5000
        self.screen_on_time = 0

        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.font = None
        self.title_font = None
        self.buttons = []
        self.message = ""
        self.message_callback = None
        self.message_font = None
        self.player_hp = 100
        self.player_max_hp = 100
        self.animation_queue = []
        self.typewriter_text = ""
        self.typewriter_index = 0
        self.typewriter_speed = 50  # ms per character
        self.last_typewriter_update = 0
        self.initialize()
        self.logger.debug(f"CombatScreen initialized with message: '{self.message}'")

    def initialize(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 14 * self.scale_factor, bold=True)
        self.title_font = pygame.font.SysFont(None, 16 * self.scale_factor, bold=True)
        self.buttons = [
            Button(75, 134, 83, 22, "attack", CombatAction.ATTACK),
            Button(75, 167, 83, 21, "flee", CombatAction.FLEE),
            Button(75, 201, 83, 22, "use item", CombatAction.USE_ITEM),
            Button(303, 134, 108, 22, "test", CombatAction.TEST),
        ]

    def scale(self, value):
        return value * self.scale_factor

    def draw_panel(self, surface, x, y, width, height, bg_color, border_color):
        pygame.draw.rect(
            surface,
            bg_color,
            (self.scale(x), self.scale(y), self.scale(width), self.scale(height)),
        )
        pygame.draw.rect(
            surface,
            border_color,
            (self.scale(x), self.scale(y), self.scale(width), self.scale(height)),
            self.scale(1),
        )

    def draw_text(self, surface, text, x, y, color, center=False, font=None):
        if font is None:
            font = self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = (self.scale(x), self.scale(y))
        else:
            text_rect.topleft = (self.scale(x), self.scale(y))
        surface.blit(text_surface, text_rect)

    def draw(self, surface):
        # Main Panel
        self.draw_panel(surface, 45, 25, 390, 219, (120, 81, 79), (94, 58, 56))

        # Text Panel
        self.draw_panel(surface, 72, 37, 339, 85, (217, 217, 217), (0, 0, 0))
        self.draw_text(surface, self.typewriter_text, 80, 45, (0, 0, 0))

        # Buttons
        for button in self.buttons:
            button.draw(surface, self.font, self.scale_factor)

        # HP Panel
        self.draw_panel(surface, 182, 134, 109, 89, (217, 217, 217), (0, 0, 0))
        self.draw_text(
            surface, "HP", 236, 144, (0, 0, 0), center=True, font=self.title_font
        )

        # HP Display Bar
        hp_percentage = self.player_hp / self.player_max_hp
        hp_width = int(75 * hp_percentage)
        self.draw_panel(surface, 199, 163, hp_width, 16, (199, 44, 44), (0, 0, 0))
        self.draw_panel(
            surface, 199 + hp_width, 163, 75 - hp_width, 16, (150, 150, 150), (0, 0, 0)
        )
        hp_text = f"{self.player_hp}/{self.player_max_hp}"
        self.draw_text(surface, hp_text, 236, 171, (0, 0, 0), center=True)

    def update(self, dt):
        current_time = pygame.time.get_ticks()

        # Handle animation queue
        while self.animation_queue and current_time >= self.animation_queue[0].delay:
            event = self.animation_queue.pop(0)
            self.logger.debug(f"Executing animation event: {event.action.__name__}")
            event.action(*event.args)

        # Update typewriter effect
        if self.typewriter_index < len(self.message):
            if current_time - self.last_typewriter_update > self.typewriter_speed:
                self.typewriter_text += self.message[self.typewriter_index]
                self.typewriter_index += 1
                self.last_typewriter_update = current_time
                self.logger.debug(f"Typewriter updated: '{self.typewriter_text}'")
                if self.message == self.typewriter_text:
                    self.logger.debug(f"Typewriter animation finished.")
                    self.on_message_animation_complete()

        if current_time - self.elapsed_log_time > self.log_interval:
            self.logger.debug(
                f"Updating screen (dt: {dt:.2f}ms, total screen time: {self.screen_on_time:.2f}ms)"
            )
            self.logger.debug(
                f"Update: current_time={current_time}, message='{self.message}', typewriter='{self.typewriter_text}'"
            )
            self.elapsed_log_time = current_time

    def on_message_animation_complete(self):
        if self.message_callback:
            self.logger.debug(f"Calling {self.message_callback} callback")
            self.message_callback()

    def handle_event(self, event):
        for button in self.buttons:
            action = button.handle_event(event, self.scale_factor)
            if action:
                self.logger.debug(f"Button action triggered: {action}")
                if action == CombatAction.TEST:
                    self.logger.debug("Test button pressed, initiating sequence")
                    self.test_animation_sequence()
                return action
        return None

    def set_message(self, message: str, callback: Callable = None):
        self.logger.debug(f"Setting new message: '{message}'")
        self.message = message
        self.message_callback = callback
        self.typewriter_text = ""
        self.typewriter_index = 0
        self.last_typewriter_update = pygame.time.get_ticks()

    def update_player_hp(self, current_hp, max_hp):
        self.player_hp = current_hp
        self.player_max_hp = max_hp

    def test_animation_sequence(self):
        current_time = pygame.time.get_ticks()
        self.animation_queue = [
            AnimationEvent(
                current_time + 0, self.set_message, "Initiating test sequence..."
            ),
            AnimationEvent(
                current_time + 2000, self.set_message, "Prepare for combat!"
            ),
            AnimationEvent(
                current_time + 4000, self.set_message, "Blinking attack button..."
            ),
            AnimationEvent(current_time + 4000, self.blink_button, "attack", True),
            AnimationEvent(current_time + 4500, self.blink_button, "attack", False),
            AnimationEvent(current_time + 5000, self.blink_button, "attack", True),
            AnimationEvent(current_time + 5500, self.blink_button, "attack", False),
            AnimationEvent(
                current_time + 6000, self.set_message, "Test sequence complete!"
            ),
        ]
        self.logger.debug("Test animation sequence initiated")

    def blink_button(self, button_text, state):
        for button in self.buttons:
            if button.text == button_text:
                button.blink_state = state
                break


# Example usage:
if __name__ == "__main__":
    logger = logging.getLogger("CombatScreenMain")
    pygame.init()
    width, height = 480, 270
    scale_factor = 3
    screen = pygame.display.set_mode((width * scale_factor, height * scale_factor))
    pygame.display.set_caption("Combat Screen")

    combat_screen = CombatScreen(width, height, scale_factor)

    running = True
    clock = pygame.time.Clock()
    while running:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            action = combat_screen.handle_event(event)
            if action:
                print(f"Action triggered: {action}")

        combat_screen.update(dt)

        screen.fill((37, 19, 26))  # White background
        combat_screen.draw(screen)
        pygame.display.flip()

        # Log frame info
        logger.debug(f"Frame completed. FPS: {clock.get_fps():.2f}")

    pygame.quit()
