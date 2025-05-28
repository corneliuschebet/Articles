# lib/tests/test_author.py

import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.seed import seed_database

@pytest.fixture(autouse=True)
def setup():
    seed_database()

def test_create_author():
    author = Author.create("Alice Example")
    assert isinstance(author, Author)
    assert author.name == "Alice Example"
    assert author.id is not None

def test_author_articles():
    author = Author.create("Test Author")
    mag = Magazine.create("Test Mag", "Tech")
    author.add_article(mag, "Test Article 1")
    author.add_article(mag, "Test Article 2")
    articles = author.articles()
    assert len(articles) == 2
    assert articles[0].author.name == "Test Author"

def test_author_magazines():
    author = Author.create("Contributor")
    mag1 = Magazine.create("Magazine One", "Science")
    mag2 = Magazine.create("Magazine Two", "Health")
    author.add_article(mag1, "Article A")
    author.add_article(mag2, "Article B")
    mags = author.magazines()
    assert len(mags) == 2
    assert mags[0].name in ["Magazine One", "Magazine Two"]

def test_topic_areas():
    author = Author.create("Area Expert")
    mag1 = Magazine.create("Eco Mag", "Ecology")
    mag2 = Magazine.create("Tech Mag", "Technology")
    author.add_article(mag1, "Nature Now")
    author.add_article(mag2, "AI Today")
    topics = author.topic_areas()
    assert "Ecology" in topics
    assert "Technology" in topics