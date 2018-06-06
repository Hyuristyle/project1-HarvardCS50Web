import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#----------------------------------------------------------------------------------------------

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#----------------------------------------------------------------------------------------------

def main():
	f = open("books.csv")
	reader = csv.reader(f)

	# Populating the "authors" table.
	first_line = True
	Populating the "authors" table.
	for isbn, title, author, year in reader:
		if first_line:
			first_line = False
			continue

		if db.execute("SELECT * FROM authors WHERE author = :author", {"author": author}).fetchone() == None:
			db.execute("INSERT INTO authors (author) VALUES (:author)", {"author": author})
			print(f"Added author '{author}'' to table 'authors'.")

		else:
			print(f"DBInsertError: Author '{author}' is already on the table 'authors'.")
	
	db.commit()

	# Populating the "books" table.
	first_line = True
	for isbn, title, author, year in reader:
		if first_line:
			first_line = False
			continue

		if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone() == None:
			author_id = db.execute("SELECT id FROM authors WHERE author = :author",
					{"author": author}).fetchone()[0]

			db.execute("INSERT INTO books (isbn, title, author_id, year) VALUES (:isbn, :title, :author_id, :year)",
					{"isbn": isbn, "title": title, "author_id": author_id, "year": year})
			print(f"Added book 'ISBN: {isbn} | {title}' to table 'books'.")

		else:
			print(f"DBInsertError: ISBN '{isbn}' is already on the table 'books'.")
	
	db.commit()

#----------------------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
