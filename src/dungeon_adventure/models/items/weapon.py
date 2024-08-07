from dungeon_adventure.enums.item_types import ItemType, WeaponType
from dungeon_adventure.models.items import Item


class Weapon(Item):
    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        weight: float,
        weapon_type: WeaponType,
        min_damage: int,
        max_damage: int,
    ):
        super().__init__(item_id, name, description, weight, ItemType.WEAPON)
        self._weapon_type = weapon_type
        self._min_damage = min_damage
        self._max_damage = max_damage

    @property
    def weapon_type(self) -> WeaponType:
        return self._weapon_type

    @property
    def min_damage(self) -> int:
        return self._min_damage

    @property
    def max_damage(self) -> int:
        return self._max_damage

    def use(self, user):
        # TODO: Implement use weapon logic
        pass


class Sword(Weapon):
    def __init__(self, item_id: str, name: str, damage: int, weight: float):
        super().__init__(
            item_id,
            name,
            f"A sharp sword",
            weight,
            WeaponType.SWORD,
            damage,
            damage + 2,
        )


class Bow(Weapon):
    def __init__(self, item_id: str, name: str, damage: int, weight: float):
        super().__init__(
            item_id,
            name,
            f"A powerful bow",
            weight,
            WeaponType.BOW,
            damage - 1,
            damage + 1,
        )
