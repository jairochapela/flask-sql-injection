# Script para crear y poblar la base de datos SQLite:
import sqlite3

def crear_db():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR, password VARCHAR)')
        cur.execute('INSERT INTO users VALUES (?,?)', ('admin', 'admin'))
        cur.execute('INSERT INTO users VALUES (?,?)', ('user', 'user'))


if __name__ == '__main__':
    crear_db()