import pytest

from src.characters.player import Player
from src.dungeon.room import Room
from src.enums.item_types import PillarType, PotionType, WeaponType
from src.exceptions.player import InventoryFullError
from src.items.item_factory import ItemFactory


@pytest.fixture
def player():
    return Player("Test Player")


@pytest.fixture
def player_inventory(player):
    return player.inventory


@pytest.fixture
def item_factory():
    return ItemFactory()


@pytest.fixture
def sample_weapon(item_factory: ItemFactory):
    return item_factory.create_weapon("Test Weapon", WeaponType.SWORD, 20, 10)


@pytest.fixture
def sample_potion(item_factory: ItemFactory):
    return item_factory.create_potion("Sample Potion", PotionType.HEALING, 15, 1)


@pytest.fixture
def sample_pillar(item_factory: ItemFactory):
    return item_factory.create_pillar(
        PillarType.ABSTRACTION, "Abstraction Pillar", "A test pillar", 1
    )


@pytest.fixture
def heavy_weapon(item_factory: ItemFactory):
    return item_factory.create_weapon("Heavy Weapon", WeaponType.BOW, 10, 50)


@pytest.fixture
def room_with_item(sample_weapon):
    room = Room("Test Room")
    room.add_item(sample_weapon)
    return room


def test_add_item_to_inventory(player_inventory, sample_weapon):
    player_inventory.add_item(sample_weapon)
    assert player_inventory.get_item_by_id(sample_weapon.id) is not None
    assert player_inventory.get_item_quantity(sample_weapon.id) == 1


def test_add_multiple_items_to_inventory(player_inventory, sample_potion):
    player_inventory.add_item(sample_potion)
    player_inventory.add_item(sample_potion)
    assert player_inventory.get_item_quantity(sample_potion.id) == 2


def test_inventory_weight_limit(player_inventory, heavy_weapon):
    player_inventory.add_item(heavy_weapon)
    with pytest.raises(InventoryFullError):
        player_inventory.add_item(heavy_weapon)


@pytest.mark.xfail
def test_remove_item_from_inventory(player_inventory, sample_pillar):
    player_inventory.add_item(sample_pillar)
    removed_item = player_inventory.remove_item(sample_pillar)
    assert removed_item == sample_pillar
    assert player_inventory.get_item_by_id(sample_pillar.id) is None


@pytest.mark.xfail
def test_remove_nonexistent_item_from_inventory(player_inventory, sample_pillar):
    removed_item = player_inventory.remove_item(sample_pillar)
    assert removed_item is None


def test_item_removed_from_room_when_picked_up(
    player_inventory, room_with_item, sample_weapon
):
    assert sample_weapon in room_with_item.items
    player_inventory.add_item(sample_weapon)
    room_with_item.remove_item(sample_weapon)
    assert sample_weapon not in room_with_item.items
    assert player_inventory.get_item_by_id(sample_weapon.id) is not None
