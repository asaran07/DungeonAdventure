import pytest

from src.characters.player import Player
from src.enums.item_types import ItemType
from src.items.pillar import Pillar
from src.items.potion import HealingPotion, VisionPotion


class TestPlayer:
    # TODO: Write test methods for each item or includes each item.
    health_potion = HealingPotion()
    vision_potion = VisionPotion()
    abstraction_pillar = Pillar("abstraction")
    encapsulation_pillar = Pillar("encapsulation")
    inheritance_pillar = Pillar("inheritance")
    polymorphism_pillar = Pillar("polymorphism")

    # pillar = Pillar() --> Update pillar class before testing pillar

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

    def test_add_and_remove_item_from_inventory(self, new_player: Player):
        expected_string = ("Player: John\n"
                           "HP: 50\n"
                           "Inventory:\n"
                           "  healing_potion: 1 (Weight: 0.5)\n"
                           "  vision_potion: 2 (Weight: 1.0)\n"
                           "Total Weight: 1.5/50.0")
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

        # TODO: Add and test pillar item

        actual_string = adventurer_one.__str__()
        assert actual_string == expected_string

    def test_remove_non_existent_items(self, new_player: Player):
        """Testing if removing from inventory accounts for dropping non-existent items."""
        expected_string = ("Player: John\n"
                           "HP: 50\n"
                           "Inventory is empty")
        adventurer_one = new_player
        adventurer_one.remove_from_inventory(self.health_potion.name)
        actual_string = adventurer_one.__str__()
        assert actual_string == expected_string
