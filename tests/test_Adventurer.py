import pytest
from src.Adventurer import Adventurer


@pytest.fixture
def new_adventurer():
    return Adventurer()
def test_to_string():
    """METHOD NOT COMPLETE YET: This doesn't test the last parameter, list of pillars, but tests the other
    attributes."""
    expected_string = ("Name: John\n"
                       "Hit Points: 75\n"
                       "Healing Potions: 1\n"
                       "Vision Potions: 0")
    adventurer_one = Adventurer("John", 75, 1,
                                0)
    actual_string = adventurer_one.to_string()
    #NOTE: switching these around changes what is shown as expected vs actual
    assert actual_string == expected_string

def test_use_health_potion():
    """Test method for use_health_potion. ADJUST THIS METHOD(to match above) WHEN PILLAR IS IMPLEMENTED"""
    expected_string = ("Name: John\n"
                       "Hit Points: 65\n"
                       "Healing Potions: 0\n"
                       "Vision Potions: 0")
    adventurer_one = Adventurer("John", 50,
                                1,0)
    adventurer_one.use_health_potion() #this should update Hit points AND number of healing potions
    actual_string = adventurer_one.to_string()
    # NOTE: switching these around changes what is shown as expected vs actual
    assert actual_string == expected_string
