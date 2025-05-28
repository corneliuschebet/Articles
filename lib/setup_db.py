# scripts/setup_db.py

from lib.db.connection import get_connection

def run_schema():
    conn = get_connection()
    with open("lib/db/schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("✅ Database schema created successfully!")

if __name__ == "__main__":
    run_schema()