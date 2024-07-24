from typing import List, Optional

from src.dungeon.room import Room
from src.items.pillar import Pillar
from src.items.item import Item
from src.items.potion import HealingPotion, VisionPotion


class Player:
    """Represents the player / adventurer."""
    # creating class level variables of items to prevent object mismatch
    _healing_potion: HealingPotion = HealingPotion()
    _vision_potion: VisionPotion = VisionPotion()
    _abstraction_pillar = Pillar("abstraction")
    _encapsulation_pillar = Pillar("encapsulation")
    _inheritance_pillar = Pillar("inheritance")
    _polymorphism_pillar = Pillar("polymorphism")

    def __init__(
            self,
            name: str = "John",
            hit_points: int = 50,
            total_healing_potions: int = 1,
            total_vision_potions: int = 0,
            pillars_found: Optional[List[Pillar]] = None,
    ) -> None:
        """
        Constructor for player Class

        :param str name: Name of player
        :param int hit_points: health of the player
        :param int total_healing_potions: Number of healing potions
        :param int total_vision_potions: Number of vision potions
        :param List pillars_found: List of pillars found
        """
        self._name = name
        self._hit_points = (
            hit_points  # 75-100; ***should be randomly generated between 75 & 100***
        )
        self._total_healing_potions = total_healing_potions
        self._total_vision_potions = total_vision_potions
        self._pillars_found: List[Pillar] = (
            pillars_found  # list of pillar pieces found(4 total/possible)
        )
        self.current_room: Optional[Room] = None

        # player inventory will initially be empty list, append and remove items as needed
        self._player_inventory: List = []

        # assign parameter values to (initially empty) player inventory
        self._assign_inventory()

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

    def add_to_inventory(self, item: Item) -> None:
        """This adds an item to the players inventory."""
        # if there is an item in the room, player is able to pick the item up(add to inventory)
        # keeping track of total vision & healing potions as well as pillars:
        if item.name == "healing_potion":
            self._total_healing_potions += 1
            self._player_inventory.append(self._healing_potion)
        elif item.name == "vision_potion":
            self._total_vision_potions += 1
            self._player_inventory.append(self._vision_potion)
        elif item.name == "Pillar":
            self._pillars_found.append(Pillar(item.name))
            self._player_inventory.append(item)  # <-- SHOULD FIX THIS!

        # maybe add something so that if the item isn't valid, display something? or do nothing
        # removing from room's list will be implemented somewhere later**

    def drop_from_inventory(self, item: Item) -> None:
        # if there is an item in the room, player is able to drop the item (add to room's list of items)
        if item.name == "healing_potion":
            # check amount of healing potions
            if self._total_healing_potions == 0:
                return  # return nothing--> in order to skip the method
            self._total_healing_potions -= 1
            self._player_inventory.remove(self._healing_potion)
        elif item.name == "vision_potion":
            if self._total_vision_potions == 0:  # skip the method
                return
            self._total_vision_potions -= 1
            self._player_inventory.remove(self._vision_potion)
        elif item.name == "pillar":
            self._pillars_found.remove(Pillar(item.name))
            self._player_inventory.remove(item)  # <-- SHOULD FIX THIS
        # removing from room's list will be implemented somewhere later**

    def _pillars_to_string(self) -> str:
        """This helper method helps print the pillars that the player has found."""
        pillars = ""
        for pillar in self._pillars_found:
            pillars += pillar.get_name() + " "

        return pillars

    def _assign_inventory(self) -> None:
        """This helper method creates an inventory based on the player parameter values."""
        # ex: if player was created with 1 healing potion, add a healing potion to inventory.
        if self._total_healing_potions > 0:
            num = self._total_healing_potions
            while num != 0:
                self._player_inventory.append(self._healing_potion)
                num -= 1
        elif self._total_vision_potions > 0:
            num = self._total_vision_potions
            while num != 0:
                self._player_inventory.append(self._vision_potion)
                num -= 1

    def inventory_to_string(self) -> str:
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
