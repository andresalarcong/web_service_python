import sqlite3
import json
from typing import List, Optional

from ..domain.product import Product


class ProductRepository:
    # ... __init__, _create_table, and find methods are the same ...
    def __init__(self):
        self.conn = sqlite3.connect("file::memory:?cache=shared", uri=True, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS products
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           data
                           JSON
                           NOT
                           NULL
                       )
                       """)
        self.conn.commit()

    def create(self, product: Product) -> Product:
        cursor = self.conn.cursor()

        # --- FIX IS HERE ---
        # Use model_dump_json() to serialize directly to a JSON string.
        # This correctly handles the datetime objects.
        product_json = product.model_dump_json(exclude={'id'})

        cursor.execute("INSERT INTO products (data) VALUES (?)", (product_json,))

        new_id = cursor.lastrowid
        self.conn.commit()
        product.id = new_id

        return product

    def find_by_id(self, product_id: int) -> Optional[Product]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, data FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()

        if row:
            product_data = json.loads(row["data"])
            product_data['id'] = row['id']
            return Product(**product_data)
        return None

    def find_all(self) -> List[Product]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, data FROM products")
        rows = cursor.fetchall()

        products = []
        for row in rows:
            product_data = json.loads(row["data"])
            product_data['id'] = row['id']
            products.append(Product(**product_data))
        return products

    def find_by_name(self, name: str) -> Optional[Product]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, data FROM products WHERE json_extract(data, '$.name') = ?", (name,))
        row = cursor.fetchone()

        if row:
            product_data = json.loads(row["data"])
            product_data['id'] = row['id']
            return Product(**product_data)
        return None

    def update(self, product: Product) -> Product:
        cursor = self.conn.cursor()

        # --- APPLY THE SAME FIX HERE FOR CONSISTENCY ---
        # model_dump_json() handles the updated_at datetime field correctly.
        product_json = product.model_dump_json(exclude={'id'})

        cursor.execute("UPDATE products SET data = ? WHERE id = ?", (product_json, product.id))
        self.conn.commit()
        return product

    def delete(self, product_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def close_connection(self):
        self.conn.close()