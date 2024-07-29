import pytest

from src.characters.player import Player
from src.items.pillar import AbstractionPillar, EncapsulationPillar, InheritancePillar, PolymorphismPillar
from src.items.potion import HealingPotion, VisionPotion


class TestPlayer:
    health_potion = HealingPotion()
    vision_potion = VisionPotion()
    abstraction_pillar = AbstractionPillar()
    encapsulation_pillar = EncapsulationPillar()
    inheritance_pillar = InheritancePillar()
    polymorphism_pillar = PolymorphismPillar()

    @pytest.fixture
    def new_player(self):
        return Player("John", 50)

    def test_to_string(self, new_player: Player):
        expected_string = ("Player: John\n"
                           "HP: 50\n"
                           "Inventory is empty")
        adventurer_one = new_player
        actual_string = adventurer_one.__str__()
        # NOTE: switching these around changes what is shown as expected vs actual
        assert actual_string == expected_string

    def test_use_health_potion(self, new_player: Player):
        expected_string = ("Player: John\n"
                           "HP: 65\n"
                           "Inventory is empty")
        adventurer_one = new_player

        adventurer_one.add_to_inventory(self.health_potion)

        # this should update Hit points AND number of healing potions from inventory
        adventurer_one.use_item(self.health_potion.name)

        actual_string = adventurer_one.__str__()
        # NOTE: switching these around changes what is shown as expected vs actual
        assert actual_string == expected_string

    def test_use_vision_potion(self, new_player: Player):
        pass  # ToDo: See how group wants the vision potion to work

    def test_add_and_remove_item_from_inventory(self, new_player: Player):
        expected_string = ("Player: John\n"
                           "HP: 50\n"
                           "Inventory:\n"
                           "  healing_potion: 1 (Weight: 0.5)\n"
                           "  vision_potion: 2 (Weight: 1.0)\n"
                           "  inheritance_pillar: 1 (Weight: 1.0)\n"
                           "  polymorphism_pillar: 1 (Weight: 1.0)\n"
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
        expected_string = ("Player: John\n"
                           "HP: 50\n"
                           "Inventory is empty")
        adventurer_one = new_player
        adventurer_one.remove_from_inventory(self.health_potion.name)
        adventurer_one.remove_from_inventory(self.abstraction_pillar.name)
        actual_string = adventurer_one.__str__()
        assert actual_string == expected_string
