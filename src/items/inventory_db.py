import sqlite3
from typing import List, Tuple

from src.items.item import Item


class InventoryDatabase:
    def __init__(self, database_path: str):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def add_item(self, item: Item, quantity: int) -> int:
        self.cursor.execute('INSERT INTO items (item_name, quantity) VALUES (?, ?)', (item.name, quantity))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_all_items(self) -> List[Tuple[int, str, int]]:
        self.cursor.execute('SELECT * FROM items')
        return self.cursor.fetchall()

    def get_item_by_id(self, item_id: int) -> Tuple[int, str, int]:
        self.cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        return self.cursor.fetchone()

    def update_item_quantity(self, item_id: int, new_quantity: int) -> None:
        self.cursor.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item_id))
        self.connection.commit()

    def close(self):
        self.connection.close()
