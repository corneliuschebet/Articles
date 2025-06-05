from db.connection import CONN, CURSOR

class Author:
    def __init__(self, name, email=None, bio=None, author_id=None):
        self.id = author_id
        self.name = name
        self.email = email
        self.bio = bio

    def save(self):
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO authors (name, email, bio) VALUES (?, ?, ?)",
                (self.name, self.email, self.bio)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute(
                "UPDATE authors SET name = ?, email = ?, bio = ? WHERE author_id = ?",
                (self.name, self.email, self.bio, self.id)
            )
            CONN.commit()

    @classmethod
    def create(cls, name, email=None, bio=None):
        author = cls(name, email, bio)
        author.save()
        return author

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        if row:
            return cls(row["name"], row["email"], row["bio"], row["author_id"])
        return None

    def articles(self):
        from lib.models.article import Article
        CURSOR.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = CURSOR.fetchall()
        return [Article(row["article_id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]

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
            return cls(row["name"], row["email"], row["bio"], row["author_id"])
        return None
