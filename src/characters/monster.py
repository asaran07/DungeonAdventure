import random
from src.characters.dungeon_character import DungeonCharacter


class Monster(DungeonCharacter):
    def __init__(self, name: str = "generic monster", hp: int = 70, min_damage: int = 15,
                 max_damage: int = 30, attack_speed: int = 2, chance_to_hit: int = 60,
                 chance_to_heal: int = 10, min_heal_points: int = 20,
                 max_heal_points: int = 40):
        self.chance_to_heal = chance_to_heal
        self.min_heal_points = min_heal_points
        self.max_heal_points = max_heal_points

        DungeonCharacter.__init__(name, hp, min_damage, max_damage,
                                  attack_speed, chance_to_hit)

    """ a Monster has a chance to heal after any attack that causes a loss of hit points 
    -- this should be checked after the Monster has been attacked and hit points have 
    been lost  """

    def heal(self):
        # Note: Still need to set a condition that calls heal when a monster takes damage
        dice_roll_to_heal = random.randint(0, 100)

        if self.hp > 0 and dice_roll_to_heal <= self.chance_to_heal:  # if heal successful
            # ex: If monster has 90% chance to heal, anything from 1 to 90 would heal
            self.gain_health()
        elif self.hp > 0 and dice_roll_to_heal > self.chance_to_hit:  # if heal unsuccessful
            # ex: If monster has 90% chance to heal, anything from 91 to 100 would not heal
            pass
        else:  # if this monster is at 0 or less hp (aka already KOed)
            pass

    def gain_health(self):
        amount: int = random.randint(self.min_heal_points, self.max_heal_points)

        self.hp += amount
