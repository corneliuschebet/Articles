# db/connection.py
import sqlite3

CONN = sqlite3.connect("db/development.db") 
CONN.row_factory = sqlite3.Row
CURSOR = CONN.cursor()
