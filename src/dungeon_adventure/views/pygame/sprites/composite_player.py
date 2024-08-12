from dungeon_adventure.models.player.player import Player
from dungeon_adventure.views.pygame.sprites.py_player import PyPlayer
from dungeon_adventure.views.pygame.room.game_room import GameRoom
import pygame


class CompositePlayer:
    def __init__(self, core_player: Player, py_player: PyPlayer):
        self.player = core_player
        self.py_player = py_player

    def initialize(self):
        self.py_player.initialize()

    def update(self, dt: int, current_room: GameRoom):
        self.py_player.update(dt, current_room)

    def move(self, dx: int, dy: int, current_room: GameRoom):
        self.py_player.move(dx, dy, current_room)

    def draw_hitbox(self, surface: pygame.Surface):
        self.py_player.draw_hitbox(surface)

    def draw_debug_info(self, surface: pygame.Surface):
        self.py_player.draw_debug_info(surface)

    # Delegate methods to Player
    @property
    def name(self):
        return self.player.name

    @property
    def inventory(self):
        return self.player.inventory

    @property
    def hero(self):
        return self.player.hero

    @property
    def current_room(self):
        return self.player.current_room

    @current_room.setter
    def current_room(self, room):
        self.player.current_room = room

    def use_item(self, item):
        return self.player.use_item(item)

    def use_item_by_id(self, item_id):
        return self.player.use_item_by_id(item_id)

    def equip_weapon(self, weapon):
        return self.player.equip_weapon(weapon)

    def heal(self, heal_amount):
        self.player.heal(heal_amount)

    def __str__(self):
        return str(self.player)

    # PyPlayer specific properties
    @property
    def rect(self):
        return self.py_player.rect

    @property
    def image(self):
        return self.py_player.image

    @property
    def sprite(self):
        return self.py_player
