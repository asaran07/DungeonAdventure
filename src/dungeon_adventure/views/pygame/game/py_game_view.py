import logging
from typing import Dict, Optional

import pygame

from dungeon_adventure.models.inventory.inventory import Inventory
from dungeon_adventure.views.pygame.combat.combat_screen import CombatScreen
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
        self.window_width: int = window_width
        self.window_height: int = window_height
        self.scale_factor: int = scale_factor
        self.minimap: Optional[MiniMap] = None
        self.inventory_display: Optional[InventoryDisplay] = None
        self.room_items_display: Optional[RoomItemsDisplay] = None
        self.controls_display: Optional[ControlsDisplay] = None
        self.combat_screen: Optional[CombatScreen] = None

        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self._minimap_visible: bool = True
        self._combat_screen_visible: bool = False
        self._controls_visible: bool = False
        self._room_items_visible: bool = False
        self._inventory_visible: bool = False

    def initialize(self) -> None:
        """Initialize all UI components."""
        self.minimap = MiniMap(
            self.window_width * self.scale_factor,
            self.window_height * self.scale_factor,
        )
        self.inventory_display = InventoryDisplay(
            self.window_width, self.window_height, self.scale_factor
        )
        self.room_items_display = RoomItemsDisplay(self.scale_factor)
        self.controls_display = ControlsDisplay(
            self.window_width * self.scale_factor,
            self.window_height * self.scale_factor,
        )

    def update(self, current_room: GameRoom, room_dict: Dict[str, GameRoom]) -> None:
        """
        Update the state of UI components.

        :param current_room: The current GameRoom the player is in
        :param room_dict: Dictionary of all GameRooms in the game
        """
        self.minimap.update(current_room, room_dict)
        self.room_items_display.update(current_room.room)

    def draw(self, screen: pygame.Surface, player_inventory: Inventory) -> None:
        """
        Draw all UI components to the screen.

        :param screen: The pygame surface to draw on
        :param player_inventory: The player's inventory
        """
        if self._minimap_visible:
            self.minimap.draw(screen)
        # if self._combat_screen_visible:
        #     self.combat_screen.draw(screen)
        if self._inventory_visible:
            self.inventory_display.draw(screen, player_inventory)
            self.inventory_display.item_details_popup.draw(screen)
        if self._room_items_visible:
            self.room_items_display.draw(screen)
        if self._controls_visible:
            self.controls_display.draw(screen)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame events for UI components."""
        return self.inventory_display.handle_event(event)

    @property
    def minimap_visible(self) -> bool:
        return self._minimap_visible

    @minimap_visible.setter
    def minimap_visible(self, value: bool) -> None:
        self._minimap_visible = value
        self.logger.info(f"Minimap visibility set to {value}")

    @property
    def combat_screen_visible(self) -> bool:
        return self._combat_screen_visible

    @combat_screen_visible.setter
    def combat_screen_visible(self, value: bool) -> None:
        self._combat_screen_visible = value
        self.logger.info(f"Combat screen visibility set to {value}")

    @property
    def controls_visible(self) -> bool:
        return self._controls_visible

    @controls_visible.setter
    def controls_visible(self, value: bool) -> None:
        self._controls_visible = value
        self.logger.info(f"Controls visibility set to {value}")

    @property
    def room_items_visible(self) -> bool:
        return self._room_items_visible

    @room_items_visible.setter
    def room_items_visible(self, value: bool) -> None:
        self._room_items_visible = value
        self.logger.info(f"Room items visibility set to {value}")

    @property
    def inventory_visible(self) -> bool:
        return self._inventory_visible

    @inventory_visible.setter
    def inventory_visible(self, value: bool) -> None:
        self._inventory_visible = value
        self.logger.info(f"Inventory visibility set to {value}")

    def toggle_visibility(self, component: str) -> None:
        """
        Toggle the visibility of a UI component.

        :param component: The name of the component to toggle
        """
        self.logger.info(f"Toggling visibility of {component}", stacklevel=2)
        if component == "minimap":
            self.minimap_visible = not self.minimap_visible
        elif component == "combat_screen":
            self.combat_screen_visible = not self.combat_screen_visible
        elif component == "controls":
            self.controls_visible = not self.controls_visible
        elif component == "room_items":
            self.room_items_visible = not self.room_items_visible
        elif component == "inventory":
            self.inventory_visible = not self.inventory_visible
        else:
            self.logger.warning(
                f"Unknown component: {component} for toggling visibility"
            )
