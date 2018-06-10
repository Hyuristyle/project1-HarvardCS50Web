import os
import collections

from flask import Flask, session, render_template, request
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

# -----------------------------------------------------------------------------------------------------------------------

class Book:
	def __init__(self, title, author, isbn, average_rating, work_ratings_count, pub_date, cover):
		self.title = title
		self.author = author
		self.isbn = isbn
		self.average_rating = average_rating
		self.work_ratings_count = work_ratings_count
		self.pub_date = pub_date
		self.cover = cover

some_covers = [
				"https://spark.adobe.com/images/landing/examples/how-to-book-cover.jpg",
				"https://about.canva.com/wp-content/uploads/sites/3/2015/01/business_bookcover.png",
				"https://images.gr-assets.com/books/1405581253l/22735855.jpg",
				"http://cdn.macrumors.com/article-new/2011/08/steve_jobs_book_cover.jpg",
				"https://d28hgpri8am2if.cloudfront.net/book_images/onix/cvr9781501127625/steve-jobs-9781501127625_hr-back.jpg"
			]

search_results = []

for i in range(8):
	try:
		exec(f"new_book{i} = Book(title = 'Harry Potter and the Philosophers Stone', author = 'Oogie Boogie', isbn = '98374283423X', average_rating = 3.5, work_ratings_count = 28, pub_date = 2018, cover = some_covers[{i}]); search_results.append(new_book{i})")

	except IndexError:
		exec(f"new_book{i} = Book(title = 'The Amazing Uga Buga', author = 'Oogie Boogie', isbn = '98374283423X', average_rating = 3.5, work_ratings_count = 28, pub_date = 2018, cover = 'http://colorlava.com/wp-content/uploads/2012/11/Classic-Red-Book-Cover-520x760.jpg'); search_results.append(new_book{i})")

# -----------------------------------------------------------------------------------------------------------------------
# Pages

# Misc.
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/Home")
def home():
	return render_template("home.html")

#@app.route("/Search/<string:search_term>")
@app.route("/Search", methods=["POST"])
def search():
	search_term = request.form.get("SearchBarInput")
	return render_template("search_results.html", search_results = search_results, search_term = search_term)

@app.route("/Book/<string:isbn>")
def book(isbn):
	user_reviewed = False

	return render_template("book.html", book = search_results[0], user_reviewed = user_reviewed)

@app.route("/Book/<string:isbn>/NewReview")
def new_review(isbn):
	return render_template("review_submission.html", book = search_results[0])

@app.route("/Book/<string:isbn>/NewReview/submit")
def new_review_submit(isbn):
	return render_template("book.html")

@app.route("/Author/<string:name>")
def author(name):
	return render_template("search_results.html")

@app.route("/Year/<int:pub_date>")
def pub_date(pub_date):
	return render_template("search_results.html")

# Users
@app.route("/Register")
def user_register():
	return render_template("register.html")

@app.route("/Register/submit")
def user_register_submit():
	return render_template("home.html")

@app.route("/MyReviews")
def user_reviews():
	return render_template("search_results.html")

@app.route("/Settings")
def user_settings():
	return render_template("user_settings.html")

@app.route("/Logout")
def logout():
	return render_template("index.html")

#
@app.route("/404")
def content_not_found():
	return render_template("error_404.html")

# -----------------------------------------------------------------------------------------------------------------------
# API

@app.route("/api/<string:isbn>")
def api_isbn(isbn):
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "4e2qojOvwwXtmXlzRdQw", "isbns": isbn})
	return str(res.json()) + "<br>" + str(res.json()["books"][0]["isbn"])

#@app.route("api/404")
#def api_isbn_not_found():
#	return "404"