import os

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import requests

from books import *

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

#-----------------------------------------------------------------------------------------------------------------------
# Fake User (temp)
class User:
	def __init__(self, user_id, name, username, password):
		self.user_id = user_id
		self.name = name
		self.username = username
		self.password = password

fake_user = User(0, "Hyuri Pimentel", "Hyuri.Pimentel", "ugabuga")

#-----------------------------------------------------------------------------------------------------------------------
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
	#TODO: Add sorting capabilities

	search_term = request.form.get("SearchBarInput")

	books = get_books(search_term, search_by = "title")

	return render_template("search_results.html", search_results = books, search_term = search_term)

@app.route("/Book/<string:isbn>")
def book(isbn):
	# TODO: Add option to delete a review

	book_data = get_book_data(isbn, cover_size = "large")

	if book_data is None:
		return render_template("error_404.html", info = {"type": "book", "message": isbn}, search_term = isbn)

	user_reviewed = False

	return render_template("book.html", book = book_data, user_reviewed = user_reviewed, search_term = book_data["title"])

@app.route("/Book/<string:isbn>/NewReview")
def new_review(isbn, text_area = None):
	# TODO:
	# Add session support, to allow the user to continue writing
	# their review in the case they leave the page by mistake or intentionally

	book_data = get_book_data(isbn, cover_size = "medium")

	if book_data is None:
		return render_template("error_404.html", info = {"type": "book", "message": isbn})

	return render_template("review_submission.html", book = book_data, user = fake_user, text_area = text_area, search_term = book_data["title"])

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
	books = get_books(name, search_by = "author")
	
	return render_template("search_results.html", search_results = books, search_term = name)

@app.route("/Year/<int:year>")
def year(year):
	books = get_books(year, search_by = "year")

	if books is None:
		return render_template("search_results.html", search_results = None)
	
	return render_template("search_results.html", search_results = books, search_term = year)

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
	return render_template("error_404.html"), 404

#-----------------------------------------------------------------------------------------------------------------------
# API

@app.route("/api/<string:isbn>")
def API_isbn(isbn):
	book_data = db.execute("SELECT title, author_id, year FROM books WHERE isbn = :isbn LIMIT 1", {"isbn": isbn}).fetchone()

	if book_data is None:
		return jsonify({"error": "isbn not found"}), 422

	author = db.execute("SELECT name FROM authors WHERE id = :author_id LIMIT 1", {"author_id": book_data.author_id}).fetchone()[0]
	
	return jsonify({
			"title": book_data["title"],
			"author": author,
			"year": book_data["year"],
			"isbn": isbn,
			"review_count": get_ratings_count(isbn),
			"average_score": get_average_rating(isbn)
		})

@app.route("/api/not_found")
def API_not_found():
	return jsonify({"error": "isbn not found in our database."}), 422