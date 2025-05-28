# scripts/run_queries.py

from lib.models.author import Author
from lib.models.article import Article
from lib.models.magazine import Magazine

def show_articles_by_author_name(name):
    print(f"\nArticles by author: {name}")
    authors = [a for a_id in range(1, 10) if (a := Author.find_by_id(a_id)) and a.name == name]
    if not authors:
        print("No such author.")
        return
    author = authors[0]
    for article in author.articles():
        print(f"- {article.title} in {article.magazine.name}")

def show_magazine_contributors(mag_id):
    mag = Magazine.find_by_id(mag_id)
    if not mag:
        print("Magazine not found.")
        return
    print(f"\nContributors to {mag.name}:")
    for contributor in mag.contributors():
        print(f"- {contributor.name}")

def show_top_publishers():
    print("\n[Not implemented yet] You can extend this to show top magazines by article count.")

if __name__ == "__main__":
    show_articles_by_author_name("John Doe")
    show_magazine_contributors(1)
    show_top_publishers()