from db.connection import CONN, CURSOR

class Article:
    def __init__(self, article_id, title, content, author_id, magazine_id):
        self.id = article_id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, author, magazine, content=""):
        CURSOR.execute(
            "INSERT INTO articles (title, author_id, magazine_id, content) VALUES (?, ?, ?, ?)",
            (title, author.id, magazine.id, content)
        )
        CONN.commit()
        article_id = CURSOR.lastrowid
        return cls(article_id, title, content, author.id, magazine.id)

    @classmethod
    def find_by_title(cls, title):
        CURSOR.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = CURSOR.fetchone()
        if row:
            return cls(row["article_id"], row["title"], row["content"], row["author_id"], row["magazine_id"])
        return None
