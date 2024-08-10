import pygame


class CombatScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)

    def draw(self, surface, player, monsters):
        # Drawing logic here
        pass

    def get_combat_input(self, event):
        # Handle Pygame events and return combat actions
        pass
