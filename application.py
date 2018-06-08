import os
import collections

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# ---

class Book:
	def __init__(self, title, author, isbn, average_rating, work_ratings_count, pub_date, cover):
		self.title = title
		self.author = author
		self.isbn = isbn
		self.average_rating = average_rating
		self.work_ratings_count = work_ratings_count
		self.pub_date = pub_date
		self.cover = cover

new_book = Book(
					title = "The Amazing Uga Buga",
					author = "Oogie Boogie",
					isbn = "98374283423X",
					average_rating = 3.5,
					work_ratings_count = 28,
					pub_date = 2018,
					cover = "http://colorlava.com/wp-content/uploads/2012/11/Classic-Red-Book-Cover-520x760.jpg"
				)

search_results = [new_book for book in range(8)]

# ---

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/Home")
def home():
	return render_template("home.html")

@app.route("/Search")
def search():
	return render_template("search_results.html", search_results = search_results)

@app.route("/Book")
def book():
	return render_template("book.html", book = new_book)

@app.route("/api/<isbn>")
def api(isbn):
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "4e2qojOvwwXtmXlzRdQw", "isbns": str(isbn)})
	return str(res.json()) + "<br>" + str(res.json()["books"][0]["isbn"])