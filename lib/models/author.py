# lib/models/author.py

from lib.db.connection import get_connection

class Author:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return cls(id=author_id, name=name)

    @classmethod
    def find_by_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(id=row["id"], name=row["name"])
        return None

    def articles(self):
        from lib.models.article import Article
        return Article.find_by_author(self.id)

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        from lib.models.magazine import Magazine
        return [Magazine(id=row["id"], name=row["name"], category=row["category"]) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        return Article.create(title=title, author=self, magazine=magazine)

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["category"] for row in rows]