from db.connection import CONN, CURSOR

class Magazine:
    def __init__(self, magazine_id, name, category):
        self.id = magazine_id
        self.name = name
        self.category = category

    def save(self):
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE magazine_id = ?",
                (self.name, self.category, self.id)
            )
            CONN.commit()

    @classmethod
    def create(cls, name, category):
        mag = cls(None, name, category)
        mag.save()
        return mag

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
        # unique authors who wrote articles for this magazine
        from lib.models.author import Author
        query = """
            SELECT DISTINCT au.author_id, au.name, au.email, au.bio
            FROM authors au
            JOIN articles ar ON au.author_id = ar.author_id
            WHERE ar.magazine_id = ?
        """
        CURSOR.execute(query, (self.id,))
        rows = CURSOR.fetchall()
        return [Author(row["name"], row["email"], row["bio"], row["author_id"]) for row in rows]

    def article_titles(self):
        CURSOR.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = CURSOR.fetchall()
        return [row["title"] for row in rows]

    def contributing_authors(self):
        # Alias for contributors (if test expects)
        return self.contributors()

    @classmethod
    def with_multiple_authors(cls):
        # Magazines with > 1 unique author
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
