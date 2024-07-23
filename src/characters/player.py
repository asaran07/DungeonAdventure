from typing import List, Optional

from src.dungeon.room import Room
from src.items.pillar import Pillar
from src.items.item import Item


class Player:

    def __init__(
        self,
        name: str,
        hit_points: int,
        total_healing_potions: int,
        total_vision_potions: int,
        pillars_found: List[Pillar],
    ) -> None:
        """Constructor for player Class"""
        self._name = name
        self._hit_points = (
            hit_points  # 75-100; ***should be randomly generated between 75 & 100***
        )
        self._total_healing_potions = total_healing_potions
        self._total_vision_potions = total_vision_potions
        self._pillars_found: List[Pillar] = (
            pillars_found  # list of pillar pieces found(4 total/possible)
        )

        # player inventory will be empty list, append and pop items as needed
        self._player_inventory = []
        # self.location = room
        # player.setLocation("main entrance") --> implement in main.py? player won't have
        # access to main entrance since not made yet
        self.current_room: Optional[Room] = None

    def get_current_room(self) -> Optional[Room]:
        return self.current_room

    def get_hp(self) -> int:
        return self._hit_points

    def get_name(self) -> str:
        return self._name

    # The contents of this method may be better suited to be in the healing_potion class
    # Perhaps an implementation of this method would be to make a call to that class?
    def use_health_potion(self) -> None:
        """Uses health potion on player to increase health"""
        self._hit_points += 15  # agreed upon by team that 15 is good
        self._total_healing_potions -= 1
        # Update player inventory as well as room's list

    def move(self):
        """To be implemented"""
        # Check w/ team regarding how this is going to work --> team verdict: will come back to later
        pass

    def add_item_to_player_inventory(self, item: Item) -> None:
        # if there is an item in the room, player is able to pick the item up(add to inventory)
        self._player_inventory.append(item)

        # keeping track of total vision & healing potions as well as pillars:
        if item.get_name() == "healing_potion":
            self._total_healing_potions += 1
        # elif item.get_name() == "vision_potion":
        #     self._total_vision_potions += 1
        # elif item.get_name() == "Pillar":
        #     self._pillars_found.append(Pillar(item.get_name()))
        # removing from room's list will be implemented somewhere later**

    def drop_item_from_player_inventory(self, item: Item) -> None:
        # if there is an item in the room, player is able to drop the item (add to room's list of items)
        self._player_inventory.remove(item)
        # keeping track of total vision & healing potions as well as pillars:
        if item.get_name() == "healing_potion":
            self._total_healing_potions -= 1
        elif item.get_name() == "vision_potion":
            self._total_vision_potions -= 1
        elif item.get_name() == "pillar":
            self._pillars_found.remove(Pillar(item.get_name()))
        # removing from room's list will be implemented somewhere later**

    def _pillars_to_string(self):
        """This helper method helps print the pillars that the player has found."""
        pillars = ""
        for pillar in self._pillars_found:
            pillars += pillar.get_name() + " "

        return pillars

    def inventory_to_string(self):
        """Returns the player's inventory in a readable string format."""
        inventory = (
            "Healing Potions: "
            + str(self._total_healing_potions)
            + "\n"
            + "Vision Potions: "
            + str(self._total_vision_potions)
            + "\n"
            + "Pillars Found: "
            + self._pillars_to_string()
        )
        return inventory

    def to_string(self) -> str:
        """Turns the attributes of the player class into a readable format."""
        string = (
            "Name: "
            + self._name
            + "\n"
            + "Hit Points: "
            + str(self._hit_points)
            + "\n"
            + self.inventory_to_string()
        )
        return string
