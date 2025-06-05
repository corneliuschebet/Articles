DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS magazines;

CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    bio TEXT
);

CREATE TABLE magazines (
    magazine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE articles (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    magazine_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(author_id),
    FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id)
);
