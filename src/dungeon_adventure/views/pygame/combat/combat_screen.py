import logging
from typing import Callable, List, Optional

import pygame
import pygame.font
from enum import Enum, auto

from dungeon_adventure.models.characters.monster import Monster


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
        self.stat_bar_callback_called = False
        self.stat_bar_callback = None
        self.logger = logging.getLogger(self.__class__.__name__)

        self.width = width
        self.height = height
        self.scale_factor = scale_factor
        self.font = None
        self.title_font = None
        self.buttons = []
        self.message = ""
        self.message_callback: Optional[Callable] = None
        self.message_font = None

        self.player_hp = 100
        self.player_max_hp = 100

        self.monster_selection_buttons = []
        self.main_buttons = None

        self.hero_title_font = pygame.font.SysFont(
            None, 20 * self.scale_factor, bold=True
        )
        self.monster_font = pygame.font.SysFont(None, 12 * self.scale_factor, bold=True)
        self.stat_bars = {"HP": 0, "Mana": 0, "XP": 0}
        self.stat_bar_visible = {"HP": False, "Mana": False, "XP": False}
        self.stat_bar_colors = {
            "HP": (199, 44, 44),
            "Mana": (44, 97, 199),
            "XP": (44, 199, 87),
        }
        self.stat_bar_animation = {"HP": None, "Mana": None, "XP": None}

        self.monster_bars = []
        self.monster_bar_animation = []

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
        self.main_buttons = [
            Button(75, 134, 83, 22, "attack", CombatAction.ATTACK),
            Button(75, 167, 83, 21, "flee", CombatAction.FLEE),
            Button(75, 201, 83, 22, "use item", CombatAction.USE_ITEM),
        ]
        self.buttons = self.main_buttons

    def create_monster_selection_buttons(self):
        self.monster_selection_buttons = [
            Button(75, 134 + i * 33, 83, 22, monster["name"], f"ATTACK_{i}")
            for i, monster in enumerate(self.monster_bars)
        ]
        self.logger.debug(
            f"Created {len(self.monster_selection_buttons)} monster selection buttons"
        )

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

        # Stats Panel
        self.draw_panel(surface, 182, 134, 109, 89, (217, 217, 217), (0, 0, 0))
        self.draw_text(surface, "Hero", 217, 141, (0, 0, 0), font=self.hero_title_font)

        # Draw stat bars
        self.draw_stat_bar(surface, "HP", 196, 163, 17, 54)
        self.draw_stat_bar(surface, "Mana", 228, 163, 17, 54)
        self.draw_stat_bar(surface, "XP", 260, 163, 17, 54)

        # Monster Stats Panel
        self.draw_panel(surface, 303, 134, 108, 89, (217, 217, 217), (0, 0, 0))

    def draw_stat_bar(self, surface, stat_type, x, y, width, height):
        if self.stat_bar_visible[stat_type]:
            fill_height = int(height * self.stat_bars[stat_type])
            pygame.draw.rect(
                surface,
                self.stat_bar_colors[stat_type],
                (
                    self.scale(x),
                    self.scale(y + height - fill_height),
                    self.scale(width),
                    self.scale(fill_height),
                ),
            )
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (self.scale(x), self.scale(y), self.scale(width), self.scale(height)),
                self.scale(1),
            )

    def display_stat_bars(
        self, player, show_hp: bool, show_mana: bool, show_xp: bool, callback: Callable
    ):
        self.logger.debug(f"Displaying stats bars for {player.hero}")
        self.stat_bar_visible["HP"] = show_hp
        self.stat_bar_visible["Mana"] = show_mana
        self.stat_bar_visible["XP"] = show_xp

        if callback is None:
            self.logger.error("Callback passed to display_stat_bars is None")
        else:
            self.stat_bar_callback = callback
            self.logger.debug(f"Stat bar callback set: {callback}")

        self.update_stat_bars(player, self.stat_bar_callback)

    def update_stat_bars(self, player, callback: Callable):
        new_hp = player.hero.current_hp / player.hero.max_hp
        new_mana = (player.hero.level * player.hero.current_hp) / (
            player.hero.level * player.hero.max_hp
        )
        new_xp = player.hero.xp / player.hero.xp_to_next_level

        self.animate_stat_bar("HP", new_hp)
        self.animate_stat_bar("Mana", new_mana)
        self.animate_stat_bar("XP", new_xp)

        # If there are no animations to run, call the callback immediately
        if all(anim is None for anim in self.stat_bar_animation.values()):
            self.logger.debug(
                "No stat bar animations to run, calling callback immediately"
            )
            if callback:
                callback()
            else:
                self.logger.warning("Stat bar callback is None, not calling")
        else:
            pass
            # self.logger.debug("Stat bar animations started, callback will be called when complete")

    def animate_stat_bar(self, stat_type, new_value):
        if self.stat_bar_visible[stat_type] and self.stat_bars[stat_type] != new_value:
            self.stat_bar_animation[stat_type] = {
                "start": self.stat_bars[stat_type],
                "end": new_value,
                "progress": 0,
            }

    def update(self, dt):
        pass

    def handle_event(self, event):
        for button in self.buttons:
            action = button.handle_event(event, self.scale_factor)
            if action:
                self.logger.debug(f"Button action triggered: {action}")
                if action == CombatAction.ATTACK:
                    return None
                elif action in (CombatAction.FLEE, CombatAction.USE_ITEM):
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
    monster_list = [Monster()]
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
