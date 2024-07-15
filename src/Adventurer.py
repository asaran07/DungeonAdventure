# from src.Pillar import Pillar #in order to make a list of pillars
from typing import List  # allows use of list?


class Adventurer:

    def __init__(self, name, hit_points, total_healing_potions,
                 total_vision_potions) -> None:
        # pillars_found: List[Pillar] --> add as last parameter later
        """Constructor for Adventurer Class"""
        self._name = name
        self._hit_points = hit_points  # 75-100; ***should be randomly generated between 75 & 100***
        self._total_healing_potions = total_healing_potions
        self._total_vision_potions = total_vision_potions
        # self.pillars_found: List[Pillar] = [] #list of pillar pieces found(4 total/possible)

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

    def to_string(self) -> str:
        """PILLAR NOT INCLUDED YET SINCE NOT IMPLEMENTED YET, just testing
         if it is working for the other fields"""

        string = ("Name: " + self._name + "\n" +
                  "Hit Points: " + str(self._hit_points) + "\n" +
                  "Healing Potions: " + str(self._total_healing_potions) + "\n" +
                  "Vision Potions: " + str(self._total_vision_potions))

        return string
