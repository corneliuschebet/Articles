# lib/tests/test_article.py

import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

@pytest.fixture(autouse=True)
def setup():
    seed_database()

def test_create_article():
    author = Author.create("Writer Test")
    magazine = Magazine.create("Test Mag", "Science")
    article = Article.create("Amazing Discoveries", author, magazine)
    assert isinstance(article, Article)
    assert article.title == "Amazing Discoveries"
    assert article.author.name == "Writer Test"
    assert article.magazine.name == "Test Mag"

def test_find_by_author():
    author = Author.create("Article Author")
    magazine = Magazine.create("Tech Mag", "Technology")
    Article.create("AI and You", author, magazine)
    Article.create("Tech is Life", author, magazine)
    results = Article.find_by_author(author.id)
    assert len(results) == 2
    assert all(article.author.id == author.id for article in results)

def test_find_by_magazine():
    author1 = Author.create("Alice")
    author2 = Author.create("Bob")
    magazine = Magazine.create("Deep Science", "Science")
    Article.create("Genes and Cells", author1, magazine)
    Article.create("The Brain Lab", author2, magazine)
    results = Article.find_by_magazine(magazine.id)
    assert len(results) == 2
    assert all(article.magazine.id == magazine.id for article in results)