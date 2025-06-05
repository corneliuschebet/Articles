
import sqlite3

def initialize_database():
    with sqlite3.connect("articles.db") as conn:
        with open("db/schema.sql") as f:
            conn.executescript(f.read())
    print("Database initialized.")

if __name__ == "__main__":
    initialize_database()
