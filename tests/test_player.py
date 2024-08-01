import pytest

from src.characters.player import Player, InvalidPlayerAttributeError
from src.items.pillar import AbstractionPillar, EncapsulationPillar, InheritancePillar, PolymorphismPillar
from src.items.potion import HealingPotion, VisionPotion
from src.exceptions.player import InvalidPlayerActionError, InventoryError, InventoryFullError, ItemNotFoundError


class TestPlayer:
    health_potion = HealingPotion()
    vision_potion = VisionPotion()
    abstraction_pillar = AbstractionPillar()
    encapsulation_pillar = EncapsulationPillar()
    inheritance_pillar = InheritancePillar()
    polymorphism_pillar = PolymorphismPillar()

    @pytest.fixture
    def new_player(self):
        return Player("John")

    # Test getters
    @pytest.mark.skip(reason="Not implemented yet")
    def test_get_hero(self, new_player: Player):
        pass

    def test_get_name(self, new_player: Player):
        """Needs name.setter to work"""
        expected_str = "John"
        actual_str = new_player.name
        assert actual_str == expected_str

    def test_set_empty_name(self):
        with pytest.raises(InvalidPlayerAttributeError):
            empty_player = Player("")

    def test_get_weight(self, new_player: Player):
        """Requires add_to_inv() & inv_to_string() to work."""
        new_player.add_to_inventory(self.health_potion)  # .5
        new_player.add_to_inventory(self.health_potion)
        new_player.add_to_inventory(self.abstraction_pillar)  # 1
        actual = new_player.get_inventory_weight()
        expected = 2.0
        assert actual == expected

    def test_to_string(self, new_player: Player):
        expected_string = ("Player: John\n"
                           "HP: 75\n"
                           "Inventory is empty")
        adventurer_one = new_player
        actual_string = adventurer_one.__str__()
        # NOTE: switching these around changes what is shown as expected vs actual
        assert actual_string == expected_string

    @pytest.mark.skip(reason="use(potion) in potion.py not implemented yet")
    def test_use_health_potion(self, new_player: Player):
        expected_string = ("Player: John\n"
                           "HP: 90\n"
                           "Inventory is empty")
        adventurer_one = new_player

        adventurer_one.add_to_inventory(self.health_potion)

        # this should update Hit points AND number of healing potions from inventory
        adventurer_one.use_item(self.health_potion.name)

        actual_string = adventurer_one.__str__()
        # NOTE: switching these around changes what is shown as expected vs actual
        assert actual_string == expected_string

    @pytest.mark.skip(reason="Not implemented yet")
    def test_use_vision_potion(self, new_player: Player):
        pass

    def test_add_and_remove_item_from_inventory(self, new_player: Player):
        expected_string = ("Player: John\n"
                           "HP: 75\n"
                           "Inventory:\n"
                           "  Healing Potion: 1 (Weight: 0.5)\n"
                           "  Vision Potion: 2 (Weight: 1.0)\n"
                           "  Inheritance Pillar: 1 (Weight: 1.0)\n"
                           "  Polymorphism Pillar: 1 (Weight: 1.0)\n"
                           "Total Weight: 3.5/50.0")
        adventurer_one = new_player

        adventurer_one.add_to_inventory(self.health_potion)
        adventurer_one.add_to_inventory(self.health_potion)
        adventurer_one.add_to_inventory(self.health_potion)
        adventurer_one.remove_from_inventory(self.health_potion.name)
        adventurer_one.remove_from_inventory(self.health_potion.name)

        adventurer_one.add_to_inventory(self.vision_potion)
        adventurer_one.add_to_inventory(self.vision_potion)
        adventurer_one.add_to_inventory(self.vision_potion)
        adventurer_one.remove_from_inventory(self.vision_potion.name)

        adventurer_one.add_to_inventory(self.abstraction_pillar)
        adventurer_one.add_to_inventory(self.encapsulation_pillar)
        adventurer_one.add_to_inventory(self.inheritance_pillar)
        adventurer_one.add_to_inventory(self.polymorphism_pillar)
        adventurer_one.remove_from_inventory(self.abstraction_pillar.name)
        adventurer_one.remove_from_inventory(self.encapsulation_pillar.name)

        actual_string = adventurer_one.__str__()
        assert actual_string == expected_string

    def test_remove_non_existent_items(self, new_player: Player):
        """Testing if removing from inventory accounts for dropping non-existent items."""
        assert new_player.remove_from_inventory(self.health_potion.name) is None
