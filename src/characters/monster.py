from src.characters.dungeon_character import DungeonCharacter


class Monster(DungeonCharacter):
    def __init__(self, name: str, hp: int, min_damage: int, max_damage: int,
                 attack_speed: int, chance_to_hit: int, chance_to_heal: int,
                 min_heal_points: int, max_heal_points: int):
        DungeonCharacter.__init__(self, name: str, hp: int, min_damage: int, max_damage: int,
        attack_speed: int, chance_to_hit: int)
        self.chance_to_heal = chance_to_heal
        self.min_heal_points = min_heal_points
        self.max_heal_points = max_heal_points

    def heal(self):
        pass


