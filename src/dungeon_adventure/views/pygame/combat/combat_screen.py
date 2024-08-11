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
            (self._width - 1000, self._height - 500)
        )
        self.enemy_info_display = pygame.Surface(
            (self._width - 1000, self._height - 500)
        )
        self.action_display = pygame.Surface((self._width - 1000, self._height - 500))
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

        player_info_surface = pygame.font.Font(FONT_PATH + "honk.ttf", 32).render(
            "Player Info", True, WHITE
        )
        player_info_title_rect = player_info_surface.get_rect(
            midtop=(self.player_info_display.get_width() // 2, 10)
        )

        self.player_info_display.blit(player_info_surface, player_info_title_rect)
        self.display.blit(self.player_info_display, player_info_rect)

    def draw_enemy_info(self):
        pygame.draw.rect(
            self.enemy_info_display, WHITE, self.enemy_info_display.get_rect(), 2
        )

        enemy_info_rect = self.enemy_info_display.get_rect(
            bottomright=(self.display.get_width() - 20, self.display.get_height() - 20)
        )

        enemy_info_surface = pygame.font.Font(None, 40).render(
            "Enemy Info", True, WHITE
        )
        enemy_info_title_rect = enemy_info_surface.get_rect(
            midtop=(self.enemy_info_display.get_width() // 2, 10)
        )

        self.enemy_info_display.blit(enemy_info_surface, enemy_info_title_rect)
        self.display.blit(self.enemy_info_display, enemy_info_rect)

    def draw_action_display(self):
        pygame.draw.rect(self.action_display, WHITE, self.action_display.get_rect(), 2)

        action_rect = self.action_display.get_rect(
            midbottom=(self.display.get_width() // 2, self.display.get_height() - 20)
        )

        action_surface = pygame.font.Font(None, 40).render("Actions", True, WHITE)
        action_title_rect = action_surface.get_rect(
            midtop=(self.action_display.get_width() // 2, 10)
        )

        self.action_display.blit(action_surface, action_title_rect)
        self.display.blit(self.action_display, action_rect)
