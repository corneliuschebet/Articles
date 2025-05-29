## Articles Code Challenge

This project models the relationships between Authors, Articles, and Magazines using raw SQL and Python classes. Data is persisted in an SQLite database.

---

## Features

- Authors can write many articles.
- Magazines can publish many articles.
- Articles belong to one author and one magazine.
- Query methods to find, save, and relate records.
---

## Setup Instructions

1. Install dependencies (if using pipenv):
   pipenv install pytest
   pipenv shell
2. Initialize the database:
   python -m lib.scripts.setup_db   
   python -m lib.db.seed
3. Run the Tests
   pytest