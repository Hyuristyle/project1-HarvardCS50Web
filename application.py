from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session

from DB import *

import requests

from books import *
from users import *
from reviews import *

import re

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#-----------------------------------------------------------------------------------------------------------------------
# Fake User (temp)

fake_user = User(1, "Hyuri Pimentel", "Hyuristyle", "12345")

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

@app.route("/Book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
	# TODO: Add option to delete a review

	book_data = get_book_data(isbn, cover_size = "large")

	if book_data is None:
		return render_template("error_404.html", info = {"type": "book", "message": isbn}, search_term = isbn)

	reviews = get_book_reviews(isbn)

	user_review = get_user_review(isbn, fake_user.user_id)

	return render_template("book.html", book = book_data, reviews = reviews, user_review = user_review, search_term = book_data["title"])

@app.route("/Book/<string:isbn>/NewReview")
def new_review(isbn, text_area = None):
	# TODO:
	# Add session support, to allow the user to continue writing
	# their review in the case they leave the page by mistake or intentionally

	book_data = get_book_data(isbn, cover_size = "medium")

	if book_data is None:
		return render_template("error_404.html", info = {"type": "book", "message": isbn})

	return render_template("review_submission.html", book = book_data, search_term = book_data["title"])

@app.route("/Book/<string:isbn>/NewReview/submit", methods=["POST"])
def new_review_submit(isbn):
	rating = request.form.get("rating-value")
	review = request.form.get("TextArea")

	user_id = 1

	add_review(isbn, user_id, rating, review)

	book_data = get_book_data(isbn, cover_size = "medium")

	reviews = get_book_reviews(isbn)

	return redirect(url_for("book", isbn = isbn, search_term = book_data["title"]))

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
@app.route("/Login", methods=["POST"])
def user_login():
	if request.method != "POST":
		return render_template("index.html")
	
	username = request.form.get("username_login")
	password = request.form.get("password_login")

	if not authorize_user(username, password):
		return "Username or Password incorrect. Try again, please!"
	
	# TODO:
	# user_id = get_user_id(username)
	# start session/set cookies

	# TODO: send notification informing successful login
	return render_template("home.html")

@app.route("/Register", methods=["POST"])
def user_register():
	if request.method != "POST":
		return render_template("index.html")

	fullname = request.form.get("fullname_register")
	username = request.form.get("username_register")
	password = request.form.get("password_register")

	if username_exists(str(username)):
		return "Username already taken. Choose a different one, please!"

	if not valid_password(password):
		return "Password must be at least 8 characters long and contain letters, numbers, uppercase, lowercase and symbols."

	add_user(username, fullname, password)
	# TODO: start session/set cookies

	# TODO: send notification informing successful registration
	return redirect(url_for("home"))

@app.route("/MyReviews")
def user_reviews():
	return render_template("search_results.html")

@app.route("/Settings")
def user_settings():
	return render_template("user_settings.html")

@app.route("/Logout")
def user_logout():
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