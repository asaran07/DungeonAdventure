import random
from random import Random

random_hit_roll = Random(222)
# assert random_hit_roll.randint(1, 100) == 20
random_damage = Random(222)
# assert random_damage.randint(2, 5) == 5

class DungeonCharacter:
    """this class can be used with either the Hero or Monster classes"""

    def __init__(self, name: str = "generic character", hp: int = 10, min_damage: int = 1, max_damage: int = 10,
                 attack_speed: int = 1, chance_to_hit: int = 50) -> object:
        self.name = name
        self.hp = hp
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.attack_speed = attack_speed
        self.chance_to_hit = chance_to_hit

    def attack(self, opponent):
        """determines this character's attack against an opponent character"""
        dice_roll_to_hit = random.randint(1, 100)

        if self.hp > 0 and dice_roll_to_hit <= self.chance_to_hit:  #if the hit connected
            #ex: If character has 90% chance to hit, anything from 1 to 90 would hit
            opponent.lose_health()
        elif self.hp > 0 and dice_roll_to_hit > self.chance_to_hit:  #if the hit missed
            #ex: If character has 90% chance to hit, anything from 91 to 100 would miss
            pass
        else:  #if this attacking character is at 0 or less hp (aka already KOed)
            pass

    def lose_health(self):
        """determines how much health this character loses"""
        amount: int = random.randint(self.min_damage, self.max_damage)

        if amount > self.hp:
            self.hp = 0
        else:
            self.hp -= amount
