from db.connection import CONN, CURSOR
# Avoid circular imports at the top level
# from lib.models.magazine import Magazine
# from lib.models.article import Article

class Author:
    def __init__(self, author_id, name, email, bio):
        self.id = author_id
        self.name = name
        self.email = email
        self.bio = bio

    @classmethod
    def create(cls, name, email, bio):
        CURSOR.execute(
            "INSERT INTO authors (name, email, bio) VALUES (?, ?, ?)",
            (name, email, bio)
        )
        CONN.commit()
        author_id = CURSOR.lastrowid
        return cls(author_id, name, email, bio)

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        if row:
            return cls(row["author_id"], row["name"], row["email"], row["bio"])
        return None

    def magazines(self):
        from lib.models.magazine import Magazine
        query = """
            SELECT DISTINCT m.magazine_id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.magazine_id = a.magazine_id
            WHERE a.author_id = ?
        """
        CURSOR.execute(query, (self.id,))
        rows = CURSOR.fetchall()
        return [Magazine(row["magazine_id"], row["name"], row["category"]) for row in rows]

    def add_article(self, title, magazine):
        from lib.models.article import Article
        # 'magazine' param is a Magazine instance
        return Article.create(title, self, magazine)

    @classmethod
    def top_author(cls):
        query = """
            SELECT au.author_id, au.name, au.email, au.bio, COUNT(ar.article_id) AS article_count
            FROM authors au
            JOIN articles ar ON au.author_id = ar.author_id
            GROUP BY au.author_id
            ORDER BY article_count DESC
            LIMIT 1
        """
        CURSOR.execute(query)
        row = CURSOR.fetchone()
        if row:
            return cls(row["author_id"], row["name"], row["email"], row["bio"])
        return None
