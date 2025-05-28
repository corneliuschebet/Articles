# lib/db/seed.py

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Supprimer les données existantes dans le bon ordre
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM magazines")
    cursor.execute("DELETE FROM authors")
    conn.commit()

    # Créer des auteurs
    john = Author.create("John Doe")
    jane = Author.create("Jane Smith")
    bob = Author.create("Bob Johnson")

    # Créer des magazines
    tech = Magazine.create("Tech Today", "Technology")
    science = Magazine.create("Science Weekly", "Science")
    biz = Magazine.create("Business Monthly", "Business")

    # Créer des articles
    Article.create("AI in 2025", john, tech)
    Article.create("Quantum Leap", jane, science)
    Article.create("Startup Trends", bob, biz)
    Article.create("Big Data", john, tech)
    Article.create("Neuroscience Advances", jane, science)
    Article.create("Blockchain Boom", bob, tech)
    Article.create("Climate Innovation", jane, biz)

    conn.close()
    print("✅ Database seeded successfully!")

# Optionnel : pour exécuter directement ce fichier
if __name__ == "__main__":
    seed_database()