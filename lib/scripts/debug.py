# scripts/debug.py

from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine
from lib.db.seed import seed_database

seed_database()

print("\n--- All Authors ---")
for i in range(1, 10):
    author = Author.find_by_id(i)
    if author:
        print(f"{author.id}: {author.name}")

print("\n--- Articles by Author 1 ---")
author = Author.find_by_id(1)
if author:
    for article in author.articles():
        print(f"- {article.title} in {article.magazine.name}")

print("\n--- Magazines Author 1 has contributed to ---")
if author:
    for mag in author.magazines():
        print(f"- {mag.name} ({mag.category})")

print("\n--- Titles in Tech Today ---")
mag = Magazine.find_by_id(1)
if mag:
    print(mag.article_titles())

print("\n--- Top Contributors in Tech Today ---")
if mag:
    print([a.name for a in mag.contributing_authors()])