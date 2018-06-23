import os
import time
import timeit
import humanize

from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#-----------------------------------------------------------------------------------------------------------------------
# Utilities

def friendly_numbers(number, short_form = True):
	if len(str(number)) > 3 and len(str(number)) < 7:
		number_plus_k = str(number)[:len(str(number)) - 3] + "k"
		return number_plus_k

	elif len(str(number)) > 6:
		if short_form:
			items = humanize.intword(number).split(" ")
			return f"{items[0]} {items[1][:2]}"

		else:
			return humanize.intword(number)

	elif len(str(number)) < 4:
		return str(number)

# Timer Decorator
def timed(func):
	def func_wrapper(*args, **kwargs):
		start = timeit.default_timer()
		print(f"{func.__name__} Start Time: {start}")

		func(*args, **kwargs)

		end = timeit.default_timer()
		print(f"{func.__name__} End Time: {end}")

		print(f"{func.__name__} Elapsed Time: {end - start}")

	return func_wrapper

#-----------------------------------------------------------------------------------------------------------------------

def get_average_rating(isbn):
	book_id = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]
	
	average_rating = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = :book_id",
																				{"book_id": book_id}).fetchall()[0][0]
	
	if average_rating == None:
		average_rating = 0.0

	return float(average_rating)

def get_ratings_count(isbn):
	book_id = db.execute("SELECT id FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]
	
	ratings_count = db.execute("SELECT COUNT(review) FROM reviews WHERE book_id = :book_id",
																				{"book_id": book_id}).fetchall()[0][0]
	
	if ratings_count == None:
		ratings_count = 0

	return int(ratings_count)

def get_book_cover(isbn, size):
	"""Possible "size" values: "large", "medium", "small", "original" """
	print("(i) Sleeping for 0.05 seconds, to comply with OpenLibrary's Rate Limiting...")
	time.sleep(0.05)

	if requests.get(f"http://covers.openlibrary.org/b/isbn/{isbn}-S.jpg?default=false").status_code == 404:
		return url_for("static", filename = "images/no_cover_available.png")
	
	if size == "large":
		return f"http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

	elif size == "medium":
		return f"http://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"

	elif size == "small":
		return f"http://covers.openlibrary.org/b/isbn/{isbn}-S.jpg"

	elif size == "original":
		return f"http://covers.openlibrary.org/b/isbn/{isbn}.jpg"

# DESCRIPTION:
# get_description(isbn)-->"Description[...]."

# DB: user_reviewed(user_id, book_id)-->(True/False, review_id/None)

def get_book_data(isbn, cover_size = "large", get_cover = True):
	"""cover_size possible values: "large", "medium", "small", "original" """

	bookviews_book_data = db.execute("SELECT title, author_id, year FROM books WHERE isbn = :isbn LIMIT 1", {"isbn": isbn}).fetchone()

	if bookviews_book_data is None:
		return None

	author = db.execute("SELECT name FROM authors WHERE id = :author_id LIMIT 1", {"author_id": bookviews_book_data.author_id}).fetchone()[0]
	
	print("(i) Sleeping for 1 second, to comply with Goodreads' Developer Terms of Service...")
	time.sleep(1)
	goodreads_book_request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "4e2qojOvwwXtmXlzRdQw", "isbns": isbn})

	if goodreads_book_request.status_code != 200:
		raise Exception("REQUEST ERROR: Goodreads API request unsuccessful.")

	goodreads_book_data = goodreads_book_request.json()["books"][0]

	if get_cover:
		book_cover = get_book_cover(isbn, size = cover_size)

	else:
		book_cover = None
	
	return {
				"isbn": isbn,
				"title": bookviews_book_data.title,
				"bookviews_average_rating": get_average_rating(isbn),
				"bookviews_ratings_count": get_ratings_count(isbn),
				"goodreads_average_rating": float(goodreads_book_data["average_rating"]),
				"goodreads_ratings_count": humanize.intcomma(int(goodreads_book_data["work_ratings_count"])),
				"author": author,
				"year": bookviews_book_data.year,
				"description": "{{{ TODO }}}",
				"cover": book_cover
	}

def get_books(search_term, search_by = "title"):
	"""search_by possible values: "title", "author", "year", "all" """

	books_search = []

	# Search by title
	if search_by == "title":
		books_search = db.execute("SELECT * FROM books WHERE (regexp_replace(title, '[[:punct:]]', '') ILIKE regexp_replace(:title, '[[:punct:]]', '')) OR (title ILIKE :title)",
										{"title": f"%{search_term}%"}).fetchall()

	# Search by author
	elif search_by == "author":
		author_id = db.execute("SELECT id FROM authors WHERE name = :name", {"name": search_term}).fetchone()

		if author_id is None:
			books_search = []

		else:
			books_search = db.execute("SELECT * FROM books WHERE author_id = :author_id", {"author_id": author_id[0]}).fetchall()

	# Search by year
	elif search_by == "year":
		books_search = db.execute("SELECT * FROM books WHERE year = :year", {"year": search_term}).fetchall()

	if books_search is None:
		return None

	# Get book data for each book
	books = []

	for book in books_search:
		books.append(get_book_data(book.isbn, cover_size = "medium"))

	if books is []:
		return None

	return books