import random
from src.characters.dungeon_character import DungeonCharacter


class Hero(DungeonCharacter):
    def __init__(self, name: str = "generic hero", hp: int = 75, min_damage: int = 20, max_damage: int = 40,
                 attack_speed: int = 6, chance_to_hit: int = 70, chance_to_block: int = 20):
        self.chance_to_block = chance_to_block

        DungeonCharacter.__init__(name, hp, min_damage, max_damage,
                                  attack_speed, chance_to_hit)

    # Hero's will check to see if they block any incoming attack
    def block(self):
        # Note: Still need to trigger this method to react when an opponent attacks the hero
        dice_roll_to_block = random.randint(1, 100)

        if self.hp > 0 and dice_roll_to_block <= self.chance_to_block: # successful block
            # ex: If hero has 90% chance to block, anything from 1 to 90 would block
            self.block_damage()
        elif self.hp > 0 and dice_roll_to_block > self.chance_to_block: # unsuccessful block
            # ex: If hero has 90% chance to block, anything from 91 to 100 would fail to block
            pass
        else: # Hero already KOed
            pass

    def block_damage(self):
        # need to change this to nullify damage from an attack once combat system is more
        # fleshed out
        pass
