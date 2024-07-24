from typing import List, Optional

from src.dungeon.room import Room
from src.items.pillar import Pillar
from src.items.item import Item
from src.items.potion import HealingPotion


class Player:
    # testing to see if this works; creating class level variable
    _healing_potion: HealingPotion = HealingPotion()

    def __init__(
            self,
            name: str = "John",
            hit_points: int = 50,
            total_healing_potions: int = 1,
            total_vision_potions: int = 0,
            pillars_found: List[Pillar] = [],
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
        self.current_room: Optional[Room] = None

        # player inventory will initially be empty list, append and remove items as needed
        self._player_inventory: List = []

        # assign parameter values to player inventory
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
        self._player_inventory.append(item)

        # keeping track of total vision & healing potions as well as pillars:
        if item.get_name() == "healing_potion":

            self._total_healing_potions += 1
        elif item.get_name() == "vision_potion":
            self._total_vision_potions += 1
        elif item.get_name() == "Pillar":
            self._pillars_found.append(Pillar(item.get_name()))

        # maybe add something so that if the item isn't valid, display something? or do nothing
        # removing from room's list will be implemented somewhere later**

    def drop_from_inventory(self, item: Item) -> None:
        # if inventory cant find item to drop then pass
        # keeping track of total vision & healing potions as well as pillars:
        if item.get_name() == "healing_potion":
            # check amount of healing potions
            # print("\n\nSTART")
            # print("Total healing potions Before removal: " + str(self._total_healing_potions) )
            # print()
            # print("Player Inventory: " + str(self._player_inventory))
            # print()
            # print("Item parameter: " + str(item))
            if self._total_healing_potions == 0:
                pass  # nothing, skip the method
            self._total_healing_potions -= 1
            self._player_inventory.remove(self._healing_potion)
            # print()
            # print("AFTER REMOVAL:")
            # print("Total healing potions after removal: " + str(self._total_healing_potions) )
            # print()
            # print("Player Inventory: " + str(self._player_inventory))
            # print()
            # print("Item parameter: " + str(item))
            # print("END\n")
        # elif item.get_name() == "vision_potion":
        #     self._total_vision_potions -= 1
        # elif item.get_name() == "pillar":
        #     self._pillars_found.remove(Pillar(item.get_name()))
        # if there is an item in the room, player is able to drop the item (add to room's list of items)
        # self._player_inventory.remove(item)

        # removing from room's list will be implemented somewhere later**

    def _pillars_to_string(self) -> str:
        """This helper method helps print the pillars that the player has found."""
        pillars = ""
        for pillar in self._pillars_found:
            pillars += pillar.get_name() + " "

        return pillars

    def _assign_inventory(self) -> None:
        """This helper method creates an inventory based on the player parameter values."""
        # if player was created with 1 healing potion, add a healing potion to inventory.
        # print("\n\nin assign_inventory, showing numHealingPotions: " + str(self._total_healing_potions))
        if self._total_healing_potions > 0:
            num = self._total_healing_potions
            while num != 0:
                # print("\n\nin assign_inventory, test One\n")
                self._player_inventory.append(self._healing_potion)
                # print("in assign_inventory, test Two")
                num -= 1

        # print(
        #     "\n\nin assign_inventory, showing numHealingPotions after method call: " + str(self._total_healing_potions))

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
