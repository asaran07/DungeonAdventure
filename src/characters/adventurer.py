from typing import List

from src.items.pillar import Pillar


class Adventurer:

    def __init__(self, name: str, hit_points: int, total_healing_potions: int,
                 total_vision_potions: int, pillars_found: List[Pillar]) -> None:
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

    #The contents of this method may be better suited to be in the healing_potion class
    #Perhaps an implementation of this method would be to make a call to that class?
    def use_health_potion(self) -> None:
        """Uses health potion on Adventurer to increase health"""
        self._hit_points += 15  # agreed upon by team that 15 is good
        self._total_healing_potions -= 1

    def move(self):
        """To be implemented"""
        # Check w/ team regarding how this is going to work --> team verdict: will come back to later
        pass

    def to_string(self) -> str:
        """Turns the attributes of the Adventurer class into a readable format."""
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