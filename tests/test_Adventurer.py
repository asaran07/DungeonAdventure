import pytest
from src.Adventurer import Adventurer


@pytest.fixture
def new_adventurer():
    return Adventurer()


def test_to_string():
    """This doesn't test the last parameter, list of pillars, but tests the other
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
