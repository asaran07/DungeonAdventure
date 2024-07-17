from typing import List

from src.items.pillar import Pillar
from src.dungeon import Room
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

        #What should be type hint if it consists of integers and another list?
        self._adventurer_inventory = [self._total_healing_potions, self._total_vision_potions,
                                      self._pillars_found]

    """
    Delete this guide later upon finishing the Adventurer class:

    NOTABLE BEHAVIORS (from Adventurer portion of Course Project canvas page)

        Adventurer/Hero & Dungeon will need to interact:
            When Adventurer walks into a room, if there is a potion
            in the room, the Adventurer automatically picks up the potion.

                (If want?, change pickup behavior AFTER this works)

            Likewise, if there is a pit in the room, the Adventure r automatically
            falls in the pit and takes a Hit Point loss.

            *These changes obviously affect the room*

            For example, if the Adventurer walks into a room with a Healing
            Potion, the Adventurer will pick up the potion, changing the 
            Adventurers (healing) potion total, as well as changing the
            ROOM's potion total*.
    """

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

    def get_items_description(self) -> str:
        """This allows adventurer to get descriptions of items in the room."""
        #So adventurer can view descriptions of items in room
        #Here maybe just iterate through the items in the room, and for each item
        #look at its description(just "item.name" as of now) and print it


    def adventurer_pick_up_item(self, item_name: str) -> None:
        #if there is an item in the room, adventurer is able to pick the item up(add to inventory)
        #names("healing_potion" & "vision_potion" in progress and not officially named yet
        if item_name == "healing_potion":
            #increment player number of healing potion
            self._total_healing_potions += 1
            self._adventurer_inventory[0] = self._total_healing_potions
            #decrement the room's number of healing potions
                #check with group if can remove from room's list, like is room's list of items
                # supposed to be private and not accessible
        elif item_name == "vision_potion":
            #increment player number of vision potion
            self._total_vision_potions += 1
            self._adventurer_inventory[1] = self._total_vision_potions
            # decrement the room's number of vision potions:
            #   check with group if can remove from room's list, like is room's list of items
            #    supposed to be private and not accessible

        else: #item is a pillar
            #add to list of pillars
            self._pillars_found.append(Pillar(item_name))
            #update player inventory
            self._adventurer_inventory[2] = self._pillars_found
            #remove from room's list of items
                #check w/ group

    def adventurer_drop_item(self, item_name: str) -> None:
        # if there is an item in the room, adventurer is able to drop the item (add to room's list of items)
        # names("healing_potion" & "vision_potion" in progress and not officially named yet
        if item_name == "healing_potion":
            # decrement player number of healing potion
            self._total_healing_potions -= 1
            self._adventurer_inventory[0] = self._total_healing_potions

            # increment the room's number of healing potions
            # check with group if can remove from room's list, like is room's list of items
            # supposed to be private and not accessible
        elif item_name == "vision_potion":
            # decrement player number of vision potion
            self._total_vision_potions -= 1 # **BUILD SETTER METHOD TO PREVENT GOING NEGATIVE!!!!!************
            self._adventurer_inventory[1] = self._total_vision_potions

            # increment the room's number of vision potions:
            #   check with group if can remove from room's list, like is room's list of items
            #    supposed to be private and not accessible

        else:  #item is a pillar
            #Remove from list of pillars
            self._pillars_found.remove(Pillar(item_name))
            #update player inventory
            self._adventurer_inventory[2] = self._pillars_found
            #remove from room's list of items
                #check w/ group

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

