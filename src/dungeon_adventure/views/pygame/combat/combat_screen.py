import logging

import pygame

from dungeon_adventure.config import FONT_PATH

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class CombatScreen:
    def __init__(self, window_width: int, window_height: int):
        self._width = window_width
        self._height = window_height
        self._display = pygame.Surface((self._width - 50, self._height - 50))
        self.player_info_display = pygame.Surface(
            (self._width - 1000, self._height - 565)
        )
        self.enemy_info_display = pygame.Surface(
            (self._width - 1000, self._height - 565)
        )
        self.action_display = pygame.Surface((self._width - 1000, self._height - 565))
        self.combat_info_display = pygame.Surface(
            (self._width - 100, self._height // 2)
        )
        self.logger = logging.getLogger(__name__)

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, surface: pygame.Surface):
        self._display = surface

    def draw(self, screen: pygame.Surface):
        display_rect = self.draw_combat_display(screen)
        self.draw_player_info()
        self.draw_action_display()
        self.draw_enemy_info()
        self.draw_combat_info_display()
        screen.blit(self.display, display_rect)

    def draw_combat_display(self, screen: pygame.Surface):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, WHITE, self.display.get_rect(), 2)
        centering_rect = screen.get_rect()
        display_rect = self.display.get_rect(center=centering_rect.center)

        title_surface = pygame.font.Font(FONT_PATH + "honk.ttf", 48).render(
            "BATTLE", True, WHITE
        )
        title_rect = title_surface.get_rect(midtop=(self.display.get_width() / 2, 10))

        self.display.blit(title_surface, title_rect)
        return display_rect

    def draw_player_info(self):
        pygame.draw.rect(
            self.player_info_display, WHITE, self.player_info_display.get_rect(), 2
        )
        player_info_rect = self.player_info_display.get_rect(
            bottomleft=(20, self.display.get_height() - 20)
        )
        self.display_text(
            "Player Info", self.player_info_display, font_size=32, position="top"
        )
        self.display.blit(self.player_info_display, player_info_rect)

    def draw_enemy_info(self):
        pygame.draw.rect(
            self.enemy_info_display, WHITE, self.enemy_info_display.get_rect(), 2
        )
        enemy_info_rect = self.enemy_info_display.get_rect(
            bottomright=(self.display.get_width() - 20, self.display.get_height() - 20)
        )
        self.display_text(
            "Enemy Info", self.enemy_info_display, font_size=32, position="top"
        )
        self.display.blit(self.enemy_info_display, enemy_info_rect)

    def draw_action_display(self):
        pygame.draw.rect(self.action_display, WHITE, self.action_display.get_rect(), 2)
        action_rect = self.action_display.get_rect(
            midbottom=(self.display.get_width() // 2, self.display.get_height() - 20)
        )
        self.display_text("Actions", self.action_display, font_size=32, position="top")
        self.display.blit(self.action_display, action_rect)

    def draw_combat_info_display(self):
        pygame.draw.rect(
            self.combat_info_display, WHITE, self.combat_info_display.get_rect(), 2
        )
        combat_info_rect = self.combat_info_display.get_rect(
            midtop=(self.display.get_width() // 2, 70)
        )
        self.display_text(
            "Combat Info", self.combat_info_display, font_size=32, position="top"
        )
        self.display.blit(self.combat_info_display, combat_info_rect)

    def display_text(
        self,
        text: str,
        display: pygame.Surface,
        font_size: int = 24,
        color: tuple = WHITE,
        position: str = "center",
    ):
        """
        Display text on a specified surface.

        :param text: The text to display
        :param display: The pygame.Surface to draw on
        :param font_size: Font size (default 24)
        :param color: Text color (default WHITE)
        :param position: Where to position the text ('center', 'top', 'bottom', 'left', 'right')
        """
        font = pygame.font.Font(FONT_PATH + "honk.ttf", font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if position == "center":
            text_rect.center = display.get_rect().center
        elif position == "top":
            text_rect.midtop = display.get_rect().midtop
        elif position == "bottom":
            text_rect.midbottom = display.get_rect().midbottom
        elif position == "left":
            text_rect.midleft = display.get_rect().midleft
        elif position == "right":
            text_rect.midright = display.get_rect().midright
        else:
            raise ValueError(
                "Invalid position. Use 'center', 'top', 'bottom', 'left', or 'right'."
            )

        display.blit(text_surface, text_rect)

    def update_player_info(self, player_health: int, player_max_health: int):
        self.logger.debug("Updating Player Info -> {}/{}".format(player_health, player_max_health))
        self.display_text(
            f"HP: {player_health}/{player_max_health}",
            self.player_info_display,
            font_size=48,
            position="center",
        )

    def display_combat_message(self, message: str):
        self.logger.debug("Displaying Combat Message -> {}".format(message))
        self.display_text(
            message, self.combat_info_display, font_size=48, position="center"
        )
