import pygame


class KeyBindManager:
    def __init__(self):
        self.inventory_key = pygame.K_i

    def is_inventory_key(self, event: pygame.event.Event) -> bool:
        return event.type == pygame.KEYDOWN and event.key == self.inventory_key
