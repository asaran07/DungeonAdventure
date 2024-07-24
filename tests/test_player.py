import pytest

from src.characters.player import Player
from src.enums.item_types import ItemType
from src.items.potion import HealingPotion, VisionPotion


# @pytest.fixture
# def new_adventurer():
#     return Player("John", 50, 1,
#                   0, [])


def test_to_string():
    """Test method for to_string(). Requires player.inventory_to_string() to work in order to test."""
    expected_string = ("Name: John\n"
                       "Hit Points: 50\n"
                       "Healing Potions: 1\n"
                       "Vision Potions: 0\n"
                       "Pillars Found: ")
    adventurer_one = Player()
    actual_string = adventurer_one.to_string()
    # NOTE: switching these around changes what is shown as expected vs actual
    assert actual_string == expected_string


def test_use_health_potion():
    """Test method for use_health_potion(). Requires to_string() to work in order to test."""
    expected_string = ("Name: John\n"
                       "Hit Points: 65\n"
                       "Healing Potions: 0\n"
                       "Vision Potions: 0\n"
                       "Pillars Found: ")
    adventurer_one = Player()
    adventurer_one.use_health_potion()  # this should update Hit points AND number of healing potions
    actual_string = adventurer_one.to_string()
    # NOTE: switching these around changes what is shown as expected vs actual
    assert actual_string == expected_string


def test_add_and_drop_health_potion_from_inventory():
    """Test method for adventurer_drop_item. Requires player.add_to_inventory() to work."""
    expected_string = ("Name: John\n"
                       "Hit Points: 50\n"
                       "Healing Potions: 2\n"
                       "Vision Potions: 0\n"
                       "Pillars Found: ")
    adventurer = Player()  # default value in parameter for Healing potions is 1
    healing_potion = HealingPotion("healing_potion", "description", .5, 10)
    adventurer.add_to_inventory(healing_potion)
    adventurer.add_to_inventory(healing_potion)
    adventurer.add_to_inventory(healing_potion)
    adventurer.drop_from_inventory(healing_potion)
    adventurer.drop_from_inventory(healing_potion)  # should be left with 2; 2 = 1 + 3 - 2
    actual_string = adventurer.to_string()
    assert actual_string == expected_string


def test_add_and_drop_vision_potion():
    """Test method for adding a vision potion."""
    expected_string = ("Name: John\n"
                       "Hit Points: 50\n"
                       "Healing Potions: 1\n"
                       "Vision Potions: 1\n"
                       "Pillars Found: ")
    adventurer = Player()  # default value in parameter for Healing potions is 1
    vision_potion = VisionPotion("vision_potion", "description", .5)
    adventurer.add_to_inventory(vision_potion)
    adventurer.add_to_inventory(vision_potion)
    adventurer.drop_from_inventory(vision_potion)
    actual_string = adventurer.to_string()
    assert actual_string == expected_string


def test_drop_non_existent_items():
    """Testing if drop_from_inventory accounts for dropping non-existent items."""
    expected_string = ("Name: John\n"
                       "Hit Points: 50\n"
                       "Healing Potions: 0\n"
                       "Vision Potions: 0\n"
                       "Pillars Found: ")
    adventurer = Player("John", 50, 1, 0, [])
    healing_potion = HealingPotion()
    vision_potion = VisionPotion()
    adventurer.drop_from_inventory(healing_potion)
    adventurer.drop_from_inventory(vision_potion)
    # adventurer.drop_from_inventory(healing_potion)
    actual_string = adventurer.to_string()
    assert actual_string == expected_string



def test_add_pillar():
    """Test method for adding pillar."""
    pass


def test_drop_pillar():
    pass
