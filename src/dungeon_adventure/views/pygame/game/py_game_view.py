from typing import Dict, Optional

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
        self.window_width = window_width
        self.window_height = window_height
        self.scale_factor = scale_factor
        self.minimap: Optional[MiniMap] = None
        self.inventory_display: Optional[InventoryDisplay] = None
        self.room_items_display: Optional[RoomItemsDisplay] = None
        self.controls_display: Optional[ControlsDisplay] = None

    def initialize(self):
        self.minimap = MiniMap(
            self.window_width * self.scale_factor,
            self.window_height * self.scale_factor,
        )
        self.inventory_display = InventoryDisplay(
            self.window_width, self.window_height, self.scale_factor
        )
        self.room_items_display = RoomItemsDisplay(self.scale_factor)
        self.controls_display = ControlsDisplay(
            self.window_width, self.window_height, self.scale_factor
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
        self.inventory_display.item_details_popup.draw(screen)
        self.room_items_display.draw(screen)
        self.controls_display.draw(screen)

    def handle_event(
        self, event: pygame.event.Event, player_inventory: Inventory
    ) -> bool:
        return self.inventory_display.handle_event(event)

    def toggle_inventory(self):
        self.inventory_display.toggle_visibility()

    # We can add methods here for handling GUI-related input,
    # showing messages, etc., similar to what ConsoleView did
