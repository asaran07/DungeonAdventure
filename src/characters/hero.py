import random
from src.characters.dungeon_character import DungeonCharacter


class Hero(DungeonCharacter):
    def __init__(self, name: str, hp: int, min_damage: int, max_damage: int,
                 attack_speed: int, chance_to_hit: int, chance_to_block: int):
        self.chance_to_block = chance_to_block

        DungeonCharacter.__init__(name, hp, min_damage, max_damage,
                                  attack_speed, chance_to_hit)

    def block(self):
        dice_roll_to_block = random.randint(1, 100)
