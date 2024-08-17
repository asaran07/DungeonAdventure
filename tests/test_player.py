import pytest

from dungeon_adventure.enums.item_types import PotionType, WeaponType
from dungeon_adventure.exceptions.player import *
from dungeon_adventure.models.player.player import Player
from dungeon_adventure.services.item_factory import ItemFactory
from dungeon_adventure.views.pygame.room.mini_map import MiniMap


class TestPlayer:
    h_potion = ItemFactory().create_potion("Healing Potion", PotionType.HEALING, 15, .5)
    v_potion = ItemFactory().create_potion("Vision Potion", PotionType.VISION, 15, .5)
    gen_weapon = ItemFactory().create_weapon("Sword", WeaponType.SWORD, 30, 5, 100)
    # minimap = MiniMap(100, 100)

    @pytest.fixture
    def new_player(self):
        return Player("John")

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

    def test_get_inventory(self, new_player: Player):

        new_player.inventory.add_item(self.h_potion)
        new_player.inventory.add_item(self.h_potion)
        actual_str = new_player.inventory.__str__()
        expected_str = (
            "Inventory:\n" "  Healing Potion: 2 (Weight: 1.0)\n" "Total Weight: 1.0/50.0"
        )
        assert actual_str == expected_str

    def test_equip_weapon(self, new_player: Player):
        new_player.inventory.add_item(self.gen_weapon)
        equip = new_player.equip_weapon(self.gen_weapon)
        assert equip is True

    def test_use_item(self, new_player: Player):
        new_player.inventory.add_item(self.h_potion)
        new_player.use_item(self.h_potion)
        assert new_player.use_item is True

    def test_use_item_by_id(self, new_player: Player):
        new_player.inventory.add_item(self.h_potion)
        item = new_player.inventory.get_item_by_id("ITEM_0001")
        assert item == self.h_potion

    def test_to_string(self, new_player: Player):
        expected_string = (
            "Player: John\n" "HP: 75\n" "Inventory:\n" "Total Weight: 0/50.0"
        )
        adventurer_one = new_player
        actual_string = adventurer_one.__str__()
        # NOTE: switching these around changes what is shown as expected vs actual
        assert actual_string == expected_string
