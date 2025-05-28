# lib/tests/test_magazine.py

import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

@pytest.fixture(autouse=True)
def setup():
    seed_database()

def test_create_magazine():
    mag = Magazine.create("Nature Weekly", "Nature")
    assert isinstance(mag, Magazine)
    assert mag.name == "Nature Weekly"
    assert mag.category == "Nature"

def test_articles_of_magazine():
    mag = Magazine.create("Brain Times", "Neuroscience")
    author = Author.create("Dr. Brain")
    Article.create("Neural Networks", author, mag)
    Article.create("Brain Chemistry", author, mag)
    articles = mag.articles()
    assert len(articles) == 2
    assert articles[0].magazine.id == mag.id

def test_contributors():
    mag = Magazine.create("Health News", "Health")
    a1 = Author.create("Ana")
    a2 = Author.create("Ben")
    a3 = Author.create("Cara")
    Article.create("Heart Health", a1, mag)
    Article.create("Mental Health", a2, mag)
    Article.create("Physical Health", a3, mag)
    contributors = mag.contributors()
    assert len(contributors) == 3

def test_article_titles():
    mag = Magazine.create("Eco Now", "Environment")
    author = Author.create("Eco Writer")
    Article.create("Trees", author, mag)
    Article.create("Rivers", author, mag)
    titles = mag.article_titles()
    assert "Trees" in titles
    assert "Rivers" in titles

def test_contributing_authors():
    mag = Magazine.create("Big Think", "Ideas")
    author = Author.create("Alex Deep")
    Article.create("Philosophy 101", author, mag)
    Article.create("Sociology Basics", author, mag)
    Article.create("Deep Logic", author, mag)
    contributors = mag.contributing_authors()
    assert len(contributors) == 1
    assert contributors[0].name == "Alex Deep"