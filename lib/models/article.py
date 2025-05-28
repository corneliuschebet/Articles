# lib/models/article.py

from lib.db.connection import get_connection

class Article:
    def __init__(self, id=None, title=None, author=None, magazine=None):
        self.id = id
        self.title = title
        self.author = author
        self.magazine = magazine

    @classmethod
    def create(cls, title, author, magazine):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, author.id, magazine.id)
        )
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return cls(id=article_id, title=title, author=author, magazine=magazine)

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()

        from lib.models.author import Author
        from lib.models.magazine import Magazine

        articles = []
        for row in rows:
            author = Author.find_by_id(row["author_id"])
            magazine = Magazine.find_by_id(row["magazine_id"])
            articles.append(cls(id=row["id"], title=row["title"], author=author, magazine=magazine))
        return articles

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()

        from lib.models.author import Author
        from lib.models.magazine import Magazine

        articles = []
        for row in rows:
            author = Author.find_by_id(row["author_id"])
            magazine = Magazine.find_by_id(row["magazine_id"])
            articles.append(cls(id=row["id"], title=row["title"], author=author, magazine=magazine))
        return articles