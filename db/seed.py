from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from db.connection import CONN, CURSOR

def seed():
    CURSOR.execute("DELETE FROM articles")
    CURSOR.execute("DELETE FROM authors")
    CURSOR.execute("DELETE FROM magazines")
    CONN.commit()

    # Create authors with name, email, bio
    alice = Author.create("Alice Smith", "alice@example.com", "Alice is a tech journalist with over a decade of experience.")
    bob = Author.create("Bob Johnson", "bob@example.com", "Bob writes about health and wellness.")
    carol = Author.create("Carol Williams", "carol@example.com", "Carol loves travel stories and adventures.")

    # Create magazines
    tech_monthly = Magazine.create("Tech Monthly", "Technology")
    health_weekly = Magazine.create("Health Weekly", "Health")
    travel_today = Magazine.create("Travel Today", "Travel")

    # Create articles
    Article.create("AI Advances", "Content about AI...", alice.id, tech_monthly.id)
    Article.create("Health Tips", "Content about health...", bob.id, health_weekly.id)
    Article.create("Travel Hacks", "Content about travel...", carol.id, travel_today.id)

    # Add an article by a different author to the same magazine for multi-author testing
    Article.create("Future Tech", "More tech content...", bob.id, tech_monthly.id)

if __name__ == "__main__":
    seed()
