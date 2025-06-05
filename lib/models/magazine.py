from db.connection import CONN, CURSOR
# Avoid circular imports at top-level
# from lib.models.author import Author
# from lib.models.article import Article

class Magazine:
    def __init__(self, magazine_id, name, category):
        self.id = magazine_id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        CURSOR.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (name, category)
        )
        CONN.commit()
        magazine_id = CURSOR.lastrowid
        return cls(magazine_id, name, category)

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        if row:
            return cls(row["magazine_id"], row["name"], row["category"])
        return None

    @classmethod
    def find_by_category(cls, category):
        CURSOR.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = CURSOR.fetchall()
        return [cls(row["magazine_id"], row["name"], row["category"]) for row in rows]

    def contributors(self):
        from lib.models.author import Author
        query = """
            SELECT DISTINCT au.author_id, au.name, au.email, au.bio
            FROM authors au
            JOIN articles ar ON au.author_id = ar.author_id
            WHERE ar.magazine_id = ?
        """
        CURSOR.execute(query, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(row["author_id"], row["name"], row["email"], row["bio"]) for row in rows]

    def article_titles(self):
        CURSOR.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = CURSOR.fetchall()
        return [row["title"] for row in rows]

    def contributing_authors(self):
        # Alias for contributors for test compatibility
        return self.contributors()

    @classmethod
    def with_multiple_authors(cls):
        query = """
            SELECT m.magazine_id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.magazine_id = a.magazine_id
            GROUP BY m.magazine_id
            HAVING COUNT(DISTINCT a.author_id) > 1
        """
        CURSOR.execute(query)
        rows = CURSOR.fetchall()
        return [cls(row["magazine_id"], row["name"], row["category"]) for row in rows]

    @classmethod
    def article_counts(cls):
        query = """
            SELECT m.name, COUNT(a.article_id) AS article_count
            FROM magazines m
            LEFT JOIN articles a ON m.magazine_id = a.magazine_id
            GROUP BY m.magazine_id
        """
        CURSOR.execute(query)
        # Return list of dicts with keys "name" and "article_count"
        return CURSOR.fetchall()
