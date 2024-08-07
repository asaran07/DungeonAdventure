from dungeon_adventure.enums.item_types import PillarType, PotionType, WeaponType
from dungeon_adventure.models.items import AbstractionPillar, Bow, EncapsulationPillar, HealingPotion, \
    InheritancePillar, Pillar, PolymorphismPillar, Potion, \
    Sword, UtilityItem, Weapon


class ItemFactory:
    def __init__(self):
        self._item_counter = 0

    def _generate_item_id(self):
        self._item_counter += 1
        return f"ITEM_{self._item_counter:04d}"

    def create_weapon(
        self, name: str, weapon_type: WeaponType, damage: int, weight: float
    ) -> Weapon:
        item_id = self._generate_item_id()

        if weapon_type == WeaponType.SWORD:
            return Sword(item_id, name, damage, weight)
        elif weapon_type == WeaponType.BOW:
            return Bow(item_id, name, damage, weight)
        else:
            return Weapon(
                item_id,
                name,
                f"A {weapon_type.name.lower()}",
                weight,
                weapon_type,
                damage,
                damage + 2,
            )

    def create_potion(
        self, name: str, potion_type: PotionType, effect_value: int, weight: float
    ) -> Potion:
        item_id = self._generate_item_id()

        if potion_type == PotionType.HEALING:
            return HealingPotion(item_id, name, effect_value, weight)
        else:
            return Potion(
                item_id,
                name,
                f"A {potion_type.name.lower()} potion",
                weight,
                potion_type,
            )

    def create_pillar(
        self,
        pillar_type: PillarType,
        name: str,
        description: str,
        weight: float = 1.0,
    ) -> Pillar:
        item_id = self._generate_item_id()
        print(f"Received pillar_type: {pillar_type}")
        if pillar_type == PillarType.ABSTRACTION:
            return AbstractionPillar(item_id, name, description, weight)
        elif pillar_type == PillarType.ENCAPSULATION:
            return EncapsulationPillar(item_id, name, description, weight)
        elif pillar_type == PillarType.INHERITANCE:
            return InheritancePillar(item_id, name, description, weight)
        elif pillar_type == PillarType.POLYMORPHISM:
            return PolymorphismPillar(item_id, name, description, weight)
        else:
            raise ValueError(f"Unknown pillar type: {pillar_type}")

    def create_utility_item(
        self,
        name: str,
        description: str,
        weight: float,
        use_type: str,
        durability: int,
        auto_use: bool = True,
    ) -> UtilityItem:
        item_id = self._generate_item_id()
        return UtilityItem(
            item_id, name, description, weight, use_type, durability, auto_use
        )

    def create_rope(self) -> UtilityItem:
        return self.create_utility_item(
            name="Rope",
            description="A sturdy rope that can help you avoid pit traps.",
            weight=2.0,
            use_type="pit",
            durability=3,
        )
