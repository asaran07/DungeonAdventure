import logging
from typing import Dict, Optional

import pygame

from dungeon_adventure.models.player.player import Player
from dungeon_adventure.views.pygame.UI.enhanced_inventory_display import (
    EnhancedInventoryDisplay,
)
from dungeon_adventure.views.pygame.UI.player_status_display import PlayerStatusDisplay
from dungeon_adventure.views.pygame.combat.combat_screen import CombatScreen
from dungeon_adventure.views.pygame.room.controls_display import ControlsDisplay
from dungeon_adventure.views.pygame.room.game_room import GameRoom
from dungeon_adventure.views.pygame.room.mini_map import MiniMap
from dungeon_adventure.views.pygame.room.player_message_display import (
    PlayerMessageDisplay,
)
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
        self.inventory_display: Optional[EnhancedInventoryDisplay] = None
        self.room_items_display: Optional[RoomItemsDisplay] = None
        self.controls_display: Optional[ControlsDisplay] = None
        self.combat_screen: Optional[CombatScreen] = None
        self.player_message_display: Optional[PlayerMessageDisplay] = None
        self.player_status_display: Optional[PlayerStatusDisplay] = None

        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self._minimap_visible: bool = True
        self._combat_screen_visible: bool = False
        self._controls_visible: bool = True
        self._room_items_visible: bool = False
        self._inventory_visible: bool = False
        self.player_message_visible: bool = False
        self._player_stats_visible: bool = True

    def initialize(self) -> None:
        """Initialize all UI components."""
        self.minimap = MiniMap(
            self.window_width * self.scale_factor,
            self.window_height * self.scale_factor,
        )
        self.inventory_display = EnhancedInventoryDisplay(
            self.window_width, self.window_height, self.scale_factor
        )
        self.room_items_display = RoomItemsDisplay(self.scale_factor)
        self.controls_display = ControlsDisplay(
            self.window_width * self.scale_factor,
            self.window_height * self.scale_factor,
        )
        self.player_message_display = PlayerMessageDisplay(
            self.window_width * self.scale_factor,
            self.window_height * self.scale_factor,
        )
        self.player_status_display = PlayerStatusDisplay(
            self.window_width * self.scale_factor,
            self.window_height * self.scale_factor,
            self.scale_factor,
        )

    def update(
        self, current_room: GameRoom, room_dict: Dict[str, GameRoom], player: Player
    ) -> None:
        """
        Update the state of UI components.

        :param player: The player
        :param current_room: The current GameRoom the player is in
        :param room_dict: Dictionary of all GameRooms in the game
        """
        self.minimap.update(current_room, room_dict)
        self.room_items_display.update(current_room.room)
        self.player_status_display.update(player)

    def draw(self, screen: pygame.Surface, player: Player) -> None:
        """
        Draw all UI components to the screen.

        :param screen: The pygame surface to draw on
        :param player: The player instance
        """
        if self._minimap_visible:
            self.minimap.draw(screen)
        # if self._combat_screen_visible:
        #     self.combat_screen.draw(screen)
        if self._inventory_visible:
            self.inventory_display.draw(screen, player)

        if self._room_items_visible:
            self.room_items_display.draw(screen)
        if self._controls_visible:
            self.controls_display.draw(screen)
        if self._player_message_visible:
            self.player_message_display.draw(screen)
        if self.player_stats_visible:
            self.player_status_display.draw(screen, player)

    def handle_event(self, event: pygame.event.Event, player: Player):
        """Handle pygame events for UI components."""
        action = self.inventory_display.handle_event(event, player)
        if action:
            action_type, item_id = action
            if action_type == "use":
                item = player.inventory.get_item_by_id(item_id)
                if item:
                    player.use_item(item, self.minimap)
            elif action_type == "drop":
                item = player.inventory.remove_item_by_id(item_id)
                if item:
                    pass
                    #  player.current_room.add_item(item)

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

    @property
    def player_stats_visible(self) -> bool:
        return self._player_stats_visible

    @player_stats_visible.setter
    def player_stats_visible(self, value: bool) -> None:
        self._player_stats_visible = value
        self.logger.info(f"Player Status visibility set to {value}")

    @property
    def player_message_visible(self) -> bool:
        return self._player_message_visible

    @player_message_visible.setter
    def player_message_visible(self, value: bool) -> None:
        self._player_message_visible = value
        self.logger.info(f"Player message visibility set to {value}")

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
        elif component == "message":
            self.player_message_visible = not self.player_message_visible
        else:
            self.logger.warning(
                f"Unknown component: {component} for toggling visibility"
            )
