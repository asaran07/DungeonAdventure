from typing import List

from src.items.pillar import Pillar
from src.items.item import Item


class Adventurer:

    def __init__(self, name: str, hit_points: int, total_healing_potions: int,
                 total_vision_potions: int, pillars_found: List[Pillar]) -> None:
        """Constructor for Adventurer Class"""
        self._name = name
        self._hit_points = hit_points  # 75-100; ***should be randomly generated between 75 & 100***
        self._total_healing_potions = total_healing_potions
        self._total_vision_potions = total_vision_potions
        self._pillars_found: List[Pillar] = pillars_found  # list of pillar pieces found(4 total/possible)

        #Adventurer inventory will be empty list, append and pop items as needed
        self._adventurer_inventory = []
        #self.location = room
        #adventurer.setLocation("main entrance") --> implement in main.py? adventurer won't have
        # access to main entrance since not made yet

    #The contents of this method may be better suited to be in the healing_potion class
    #Perhaps an implementation of this method would be to make a call to that class?
    def use_health_potion(self) -> None:
        """Uses health potion on Adventurer to increase health"""
        self._hit_points += 15  # agreed upon by team that 15 is good
        self._total_healing_potions -= 1
        #Update player inventory as well as room's list

    def move(self):
        """To be implemented"""
        # Check w/ team regarding how this is going to work --> team verdict: will come back to later
        pass

    def get_items_description(self, item_name: str) -> str:
        """This allows adventurer to get descriptions of items in the room."""
        #So adventurer can view descriptions of items in room

        healing_potion = "This potion heals the player by 5-15 health points."
        vision_potion = "This potion grants the player sight to the surrounding 8 rooms"
        pillar = "A pillar of Object Oriented Programming"

        if item_name == "healing_potion":
            description = healing_potion
        elif item_name == "vision_potion":
            description = vision_potion
        else:  #pillar is left. If more items are added, add above this?
            #Able to be rewritten to be more specific to each pillar of OO if wanted
            description = pillar
        return description

    def add_item_to_adventurer_inventory(self, item: Item) -> None:
        #if there is an item in the room, adventurer is able to pick the item up(add to inventory)
        self._adventurer_inventory.append(item)

        #keeping track of total vision & healing potions as well as pillars:
        if item.get_name() == "healing_potion":
            self._total_healing_potions += 1
        elif item.get_name() == "vision_potion":
            self._total_vision_potions += 1
        elif item.get_name() == "Pillar":
            self._pillars_found.append(Pillar(item.get_name()))
        #removing from room's list will be implemented somewhere later**

    def drop_item_from_adventurer_inventory(self, item: Item) -> None:
        # if there is an item in the room, adventurer is able to drop the item (add to room's list of items)
        self._adventurer_inventory.remove(item)
        # keeping track of total vision & healing potions as well as pillars:
        if item.get_name() == "healing_potion":
            self._total_healing_potions -= 1
        elif item.get_name() == "vision_potion":
            self._total_vision_potions -= 1
        elif item.get_name() == "Pillar":
            self._pillars_found.remove(Pillar(item.get_name()))
        # removing from room's list will be implemented somewhere later**

    def _pillars_to_string(self):
        """This helper method helps print the pillars that the adventurer has found."""
        pillars = ""
        for pillar in self._pillars_found:
            pillars += pillar.get_name() + " "

        return pillars

    def inventory_to_string(self):
        """Returns the adventurer's inventory in a readable string format."""
        inventory = ("Healing Potions: " + str(self._total_healing_potions) + "\n" +
                     "Vision Potions: " + str(self._total_vision_potions) + "\n" +
                     "Pillars Found: " + self._pillars_to_string())
        return inventory

    def to_string(self) -> str:
        """Turns the attributes of the Adventurer class into a readable format."""
        string = ("Name: " + self._name + "\n" +
                  "Hit Points: " + str(self._hit_points) + "\n" +
                  self.inventory_to_string())
        return string
