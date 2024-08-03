from src.items.item_factory import ItemFactory
from src.enums.item_types import WeaponType, PotionType
import os

factory = ItemFactory("/Users/saran/DungeonAdventure/src/SQL/inventory.sqlite")

# Create some items
sword = factory.create_weapon("Steel Sword", WeaponType.SWORD, 10, 5.0)
potion = factory.create_potion("Health Potion", PotionType.HEALING, 20, 0.5)

print(f"Created: {sword.name}, ID: {sword.id}")
print(f"Created: {potion.name}, ID: {potion.id}")
