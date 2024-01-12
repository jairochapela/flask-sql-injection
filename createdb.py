# Script para crear y poblar la base de datos SQLite:

import sqlite3

conn = sqlite3.connect('database.db')

conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
conn.execute('INSERT INTO users VALUES (?,?)', ('admin', 'admin'))
conn.execute('INSERT INTO users VALUES (?,?)', ('user', 'user'))

conn.close()
