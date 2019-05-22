# Вспомогательная функция
import sqlite3

from domain import Good


def open_db(url):
    conn = sqlite3.connect(url)
    conn.row_factory = sqlite3.Row
    return conn


# Создание схемы
def init_db(conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS goods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            qty INTEGER NOT NULL DEFAULT 0 CHECK (qty >= 0)
        );
        """)  # alt + enter -> inject language or reference
        conn.commit()


def get_all(conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, price, qty FROM goods')
        items = []
        for row in cursor:  # [Row, Row] -> [Good, Good]
            items.append(
                Good(
                    row['id'],
                    row['name'],
                    row['price'],
                    row['qty']
                )
            )
        return items


def get_by_id(conn, id):
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, name, price, qty FROM goods WHERE id = :id',
            {'id': id}
        )
        for row in cursor:
            return Good(
                row['id'],
                row['name'],
                row['price'],
                row['qty']
            )


def add(conn, good):
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO goods(name, price, qty) VALUES (:name, :price, :qty)
        """, {'name': good.name, 'price': good.price, 'qty': good.qty})
        conn.commit()


def update(conn, good):
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE goods
        SET name = :name, price = :price, qty = :qty -- запомни
        WHERE id = :id
        """, {'id': good.id, 'name': good.name, 'price': good.price, 'qty': good.qty})
        # :name берётся из {'name' <- }
        conn.commit()


def remove_by_id(conn, id):
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM goods
        WHERE id = :id
        """, {'id': id})
        conn.commit()


def sale_by_id(conn, id, count):
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE goods
        SET qty = qty - :count 
        WHERE id = :id
        """, {'id': id, 'count': count})
        # :name берётся из {'name' <- }
        conn.commit()
