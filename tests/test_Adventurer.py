import pytest
from src.Adventurer import Adventurer


@pytest.fixture
def new_adventurer():
    return Adventurer()


def test_to_string():
    """This doesn't test the last parameter, list of pillars, but tests the other
    attributes."""
    expected_string = ("John"
                       "75"
                       "1"
                       "0"
                       )

    adventurer_one = Adventurer("John", 75, 1,
                                0)

    actual_string = adventurer_one.to_string()

    assert expected_string == actual_string
