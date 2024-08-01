import pytest
from src.characters.player import Player
from src.items.weapon import Weapon
from src.items.potion import HealingPotion
from src.items.pillar import AbstractionPillar
from src.enums.item_types import WeaponType
from src.exceptions.player import InventoryFullError
from src.dungeon.room import Room


@pytest.fixture
def player():
    return Player("Test Player")


@pytest.fixture
def sample_weapon():
    return Weapon("Test Sword", "A test sword", 2.0, WeaponType.SWORD, 5, 10)


@pytest.fixture
def sample_potion():
    return HealingPotion("Test Healing Potion", "A test healing potion", 0.5, 20)


@pytest.fixture
def sample_pillar():
    return AbstractionPillar()


@pytest.fixture
def heavy_weapon():
    return Weapon("Heavy Sword", "A very heavy sword", 50.0, WeaponType.SWORD, 15, 30)


@pytest.fixture
def room_with_item(sample_weapon):
    room = Room("Test Room")
    room.add_item(sample_weapon)
    return room


def test_add_item_to_inventory(player, sample_weapon):
    player.add_to_inventory(sample_weapon)
    assert sample_weapon.name in player._inventory
    assert player._inventory[sample_weapon.name][1] == 1


def test_add_multiple_items_to_inventory(player, sample_potion):
    player.add_to_inventory(sample_potion)
    player.add_to_inventory(sample_potion)
    assert player._inventory[sample_potion.name][1] == 2


def test_inventory_weight_limit(player, heavy_weapon):
    player.add_to_inventory(heavy_weapon)
    with pytest.raises(InventoryFullError):
        player.add_to_inventory(heavy_weapon)


def test_remove_item_from_inventory(player, sample_pillar):
    player.add_to_inventory(sample_pillar)
    removed_item = player.remove_from_inventory(sample_pillar.name)
    assert removed_item == sample_pillar
    assert sample_pillar.name not in player._inventory


def test_remove_nonexistent_item_from_inventory(player):
    removed_item = player.remove_from_inventory("Nonexistent Item")
    assert removed_item is None


def test_item_removed_from_room_when_picked_up(player, room_with_item, sample_weapon):
    assert sample_weapon in room_with_item.items
    player.add_to_inventory(sample_weapon)
    room_with_item.remove_item(sample_weapon)
    assert sample_weapon not in room_with_item.items
    assert sample_weapon.name in player._inventory
