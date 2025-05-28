# lib/models/magazine.py

from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return cls(id=magazine_id, name=name, category=category)

    @classmethod
    def find_by_id(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"], category=row["category"])
        return None

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_magazine(self.id)

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author(id=row["id"], name=row["name"]) for row in rows]

    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title FROM articles WHERE magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["title"] for row in rows]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, COUNT(ar.id) as article_count FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.author import Author
        return [Author(id=row["id"], name=row["name"]) for row in rows]