import pytest

from dungeon_adventure.exceptions.player import *
from dungeon_adventure.models.player.player import Player


class TestPlayer:

    @pytest.fixture
    def new_player(self):
        return Player("John")

    # Test getters
    @pytest.mark.skip(reason="Not implemented yet")
    def test_get_hero(self, new_player: Player):
        pass

    def test_get_name(self, new_player: Player):
        expected_str = "John"
        actual_str = new_player.name
        assert actual_str == expected_str

    def test_set_empty_name(self):
        try:
            Player("")
        except InvalidPlayerAttributeError as e:
            assert str(e) == "Name cannot be empty."
        else:
            pytest.fail("InvalidPlayerAttributeError wasn't raised")

    def test_to_string(self, new_player: Player):
        expected_string = (
            "Player: John\n" "HP: 75\n" "Inventory:\n" "Total Weight: 0/50.0"
        )
        adventurer_one = new_player
        actual_string = adventurer_one.__str__()
        # NOTE: switching these around changes what is shown as expected vs actual
        assert actual_string == expected_string
