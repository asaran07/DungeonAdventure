from typing import Dict

import pygame

from dungeon_adventure.models.inventory.inventory import Inventory
from dungeon_adventure.views.pygame.room.controls_display import ControlsDisplay
from dungeon_adventure.views.pygame.room.game_room import GameRoom
from dungeon_adventure.views.pygame.room.inventory_display import InventoryDisplay
from dungeon_adventure.views.pygame.room.mini_map import MiniMap
from dungeon_adventure.views.pygame.room.room_items_display import RoomItemsDisplay


class PyGameView:
    def __init__(self, window_width: int, window_height: int, scale_factor: int):
        """
        Initialize the PyGame view with UI components.

        :param window_width: Width of the game window
        :param window_height: Height of the game window
        :param scale_factor: Scale factor for UI elements
        """
        self.minimap: MiniMap = MiniMap(window_width, window_height)
        self.inventory_display: InventoryDisplay = InventoryDisplay(
            window_width, window_height
        )
        self.room_items_display: RoomItemsDisplay = RoomItemsDisplay(scale_factor)
        self.controls_display: ControlsDisplay = ControlsDisplay(
            window_width, window_height, scale_factor
        )

    def update(self, current_room: GameRoom, room_dict: Dict[str, GameRoom]) -> None:
        """
        Update the state of UI components.

        :param current_room: The current GameRoom the player is in
        :param room_dict: Dictionary of all GameRooms in the game
        """
        self.minimap.update(current_room, room_dict)
        self.room_items_display.update(
            current_room.room
        )  # Note: using .room to get the core Room object

    def draw(self, screen: pygame.Surface, player_inventory: Inventory) -> None:
        """
        Draw all UI components to the screen.

        :param screen: The pygame surface to draw on
        :param player_inventory: The player's inventory
        """
        self.minimap.draw(screen)
        self.inventory_display.draw(screen, player_inventory)
        self.room_items_display.draw(screen)
        self.controls_display.draw(screen)

    # We can add methods here for handling GUI-related input,
    # showing messages, etc., similar to what ConsoleView did
