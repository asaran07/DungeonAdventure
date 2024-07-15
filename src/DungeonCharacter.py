import random

class DungeonCharacter:

    def __init__(self, name, hp, minDamage, maxDamage, attackSpeed, chanceToHit):
        self.name = name
        self.hp = hp
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.attackSpeed = attackSpeed
        self.chanceToHit = chanceToHit

    def attack(self, opponent):
        dice_roll_to_hit = random.randint(1, 100)

        if self.hp > 0 and dice_roll_to_hit < self.chanceToHit:
            pass
            opponent.lose_health(self.random.randint(self.minDamage, self.maxDamage))  #if the hit connected
        elif self.hp > 0 and dice_roll_to_hit >= self.chanceToHit:
            pass #if the hit missed
        else:
            pass #if this attacking character is at 0 or less hp

    def lose_health(self, amount):
        if amount > self.hp:
            self.hp = 0
        else:
            self.hp -= amount