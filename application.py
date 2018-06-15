import os
import collections
import humanize

from flask import Flask, session, render_template, request, redirect, url_for
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

# ----------------------------------------------------------------------------------------------------------------------
def human_friendly(number, short_form = True):
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

# ----------------------------------------------------------------------------------------------------------------------

class User:
	def __init__(self, user_id, name, username, password):
		self.user_id = user_id
		self.name = name
		self.username = username
		self.password = password

fake_user = User(0, "Hyuri Pimentel", "Hyuri.Pimentel", "ugabuga")

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

# for i in range(8):
# 	try:
# 		exec(f"""new_book{i} = Book(title = "Harry Potter and the Philosopher's Stone", author = "Oogie Boogie", isbn = "0590353403", average_rating = 3.5, work_ratings_count = 28, pub_date = 2018, cover = some_covers[{i}]); search_results.append(new_book{i})""")

# 	except IndexError:
# 		exec(f"""new_book{i} = Book(title = "The Amazing Uga Buga", author = "Oogie Boogie", isbn = "0590353403", average_rating = 3.5, work_ratings_count = 28, pub_date = 2018, cover = "http://colorlava.com/wp-content/uploads/2012/11/Classic-Red-Book-Cover-520x760.jpg"); search_results.append(new_book{i})""")

#---
def get_book_cover(isbn, size):
	if requests.get(f"http://covers.openlibrary.org/b/isbn/{isbn}-S.jpg?default=false").status_code == 404:
		return url_for("static", filename = "images/no_cover_found.png")
	
	if size == "large":
		return f"http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

	elif size == "medium":
		return f"http://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"

	elif size == "small":
		return f"http://covers.openlibrary.org/b/isbn/{isbn}-S.jpg"

	elif size == "original":
		return f"http://covers.openlibrary.org/b/isbn/{isbn}.jpg"

#---
goodreads_book_info = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "4e2qojOvwwXtmXlzRdQw", "isbns": "0590353403"}).json()

search_results = []
for i in range(8):
	isbn = "0590353403"
	search_results.append(
	{
				"isbn": isbn,
				"title": "Harry Potter and the Philosopher's Stone",
				"bookviews_average_rating": 3.5,
				"bookviews_ratings_count": humanize.intcomma(28),
				"goodreads_average_rating": float(goodreads_book_info["books"][0]["average_rating"]),
				"goodreads_ratings_count": humanize.intcomma(int(goodreads_book_info["books"][0]["work_ratings_count"])),
				"author": "Oogie Boogie",
				"pub_date": 2018,
				"description": "Testestest",
				"cover": get_book_cover(isbn, size = "medium")
})

# ----------------------------------------------------------------------------------------------------------------------
# Pages

# Misc.
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/Home")
def home():
	return render_template("home.html")

#@app.route("/Search/<string:search_term>")
@app.route("/Search", methods=["POST", "GET"])
def search():
	search_term = request.form.get("SearchBarInput")
	return render_template("search_results.html", search_results = search_results, search_term = search_term)

@app.route("/Book/<string:isbn>")
def book(isbn):
	user_reviewed = False

	# APIs
	# GOODREADS RATING & COUNT
	
	# COVER:
	# get_cover(isbn)-->"cover.jpg"?
	
	# DESCRIPTION:
	# get_description(isbn)-->"Description[...]."
	
	# DB: bookviews_book_info = get_bookviews_book_info(isbn)-->title, author, year, average_rating, ratings_count
	# DB: user_reviewed(user_id, book_id)-->(True/False, review_id/None)

	#book = {
	#			"title": bookviews_book_info["title"],
	#			"bookviews_average_rating": bookviews_book_info["average_rating"],
	#			"bookviews_ratings_count": bookviews_book_info["ratings_count"],
	#			"goodreads_average_rating": goodreads_book_info["average_rating"],
	#			"goodreads_ratings_count": goodreads_book_info["work_ratings_count"],
	#			"author": bookviews_book_info["author"]: ,
	#			"year": bookviews_book_info["year"]: ,
	#			"description": get_book_description(isbn),
	#			"cover": get_book_cover(isbn)
	#}

	single_book = {
				"isbn": isbn,
				"title": "Harry Potter and the Philosopher's Stone",
				"bookviews_average_rating": 3.5,
				"bookviews_ratings_count": humanize.intcomma(28),
				"goodreads_average_rating": float(goodreads_book_info["books"][0]["average_rating"]),
				"goodreads_ratings_count": humanize.intcomma(int(goodreads_book_info["books"][0]["work_ratings_count"])),
				"author": "Oogie Boogie",
				"pub_date": 2018,
				"description": "Testestest",
				"cover": get_book_cover(isbn, size = "large")
	}

	return render_template("book.html", book = single_book, user_reviewed = user_reviewed)

@app.route("/Book/<string:isbn>/NewReview")
def new_review(isbn, text_area = None):
	single_book = {
				"isbn": isbn,
				"title": "Harry Potter and the Philosopher's Stone",
				"bookviews_average_rating": 3.5,
				"bookviews_ratings_count": humanize.intcomma(28),
				"goodreads_average_rating": float(goodreads_book_info["books"][0]["average_rating"]),
				"goodreads_ratings_count": humanize.intcomma(int(goodreads_book_info["books"][0]["work_ratings_count"])),
				"author": "Oogie Boogie",
				"pub_date": 2018,
				"description": "Testestest",
				"cover": get_book_cover(isbn, size = "medium")
	}

	return render_template("review_submission.html", book = single_book, user = fake_user, text_area = text_area)

@app.route("/Book/<string:isbn>/NewReview/submit", methods=["POST"])
def new_review_submit(isbn):
	rating = request.form.get("rating-value")
	review = request.form.get("TextArea")

	if rating == "undefined":
		return redirect(url_for("new_review", isbn = "283472834", text_area = review))

	else:
		return f"Review to book {isbn} submitted by . <br> Stars: {rating} <br> Review: {review}" #render_template("book.html")

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

# ----------------------------------------------------------------------------------------------------------------------
# API

@app.route("/api/<string:isbn>")
def api_isbn(isbn):
	res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "4e2qojOvwwXtmXlzRdQw", "isbns": isbn})
	return str(res.json()) + "<br>" + str(res.json()["books"][0]["isbn"])

#@app.route("api/404")
#def api_isbn_not_found():
#	return "404"