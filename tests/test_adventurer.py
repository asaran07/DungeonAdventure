import pytest

from src.characters.adventurer import Adventurer


@pytest.fixture
def new_adventurer():
    return Adventurer("John", 75, 1,
                                0, [])

def test_to_string(new_adventurer):
    """Test method for to_string"""
    expected_string = ("Name: John\n"
                       "Hit Points: 75\n"
                       "Healing Potions: 1\n"
                       "Vision Potions: 0\n"
                       "Pillars Found: ")
    adventurer_one = new_adventurer
    actual_string = adventurer_one.to_string()
    # NOTE: switching these around changes what is shown as expected vs actual
    assert actual_string == expected_string

def test_use_health_potion(new_adventurer):
    """Test method for use_health_potion. Requires to_string() to work in order to test."""
    expected_string = ("Name: John\n"
                       "Hit Points: 65\n"
                       "Healing Potions: 0\n"
                       "Vision Potions: 0\n"
                       "Pillars Found: ")
    adventurer_one = new_adventurer
    adventurer_one.use_health_potion()  # this should update Hit points AND number of healing potions
    actual_string = adventurer_one.to_string()
    # NOTE: switching these around changes what is shown as expected vs actual
    assert actual_string == expected_string

#def test_adventurer_pick_up_item():
