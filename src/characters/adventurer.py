from typing import List

from src.items.pillar import Pillar


class Adventurer:

    def __init__(self, name, hit_points, total_healing_potions,
                 total_vision_potions, pillars_found: List[Pillar]) -> None:
        """Constructor for Adventurer Class"""
        self._name = name
        self._hit_points = hit_points  # 75-100; ***should be randomly generated between 75 & 100***
        self._total_healing_potions = total_healing_potions
        self._total_vision_potions = total_vision_potions
        self._pillars_found: List[Pillar] = pillars_found  # list of pillar pieces found(4 total/possible)

    """
    Delete this guide later upon finishing the Adventurer class:

    NOTABLE BEHAVIORS (from Adventurer portion of Course Project canvas page)

        Adventurer/Hero & Dungeon will need to interact:
            When Adventurer walks into a room, if there is a potion
            in the room, the Adventurer automatically picks up the potion.

                (If want?, change pickup behavior AFTER this works)

            Likewise, if there is a pit in the room, the Adventurer automatically
            falls in the pit and takes a Hit Point loss.

            *These changes obviously affect the room*

            For example, if the Adventurer walks into a room with a Healing
            Potion, the Adventurer will pick up the potion, changing the 
            Adventurers (healing) potion total, as well as changing the
            ROOM's potion total*.
    """

    def use_health_potion(self) -> None:
        """Uses health potion on Adventurer to increase health"""
        self._hit_points += 15  # currently 15, can change later? check w/ team
        self._total_healing_potions -= 1

    def use_vision_potion(self) -> None:
        # Check w/ team regarding how this is going to work
        """Should allow adventurer to see more?"""
        pass

    def move(self):
        """To be implemented"""
        # Check w/ team regarding how this is going to work
        pass

    def to_string(self) -> str:
        """PILLAR NOT INCLUDED YET SINCE NOT IMPLEMENTED YET, just testing
         if it is working for the other fields"""
        pillar_string = self._pillars_found  # default to display the list
        # If no pillars have been found, maybe display message?
        no_pillars = "No pillars have been found yet!"
        if len(self._pillars_found) == 0:
            # if list of pillars Adventurer has is empty, display no_pillars message
            pillar_string = no_pillars

        string = ("Name: " + self._name + "\n" +
                  "Hit Points: " + str(self._hit_points) + "\n" +
                  "Healing Potions: " + str(self._total_healing_potions) + "\n" +
                  "Vision Potions: " + str(self._total_vision_potions) + "\n" +
                  "Pillars Found: " + pillar_string)

        return string
