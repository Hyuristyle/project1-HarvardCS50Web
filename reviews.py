from DB import *

from books import get_book_id
from users import get_user_id
from users import get_user_fullname

#-----------------------------------------------------------------------------------------------------------------------

def add_review(isbn, username, rating, review):
	book_id = get_book_id(isbn)
	user_id = get_user_id(username)

	db.execute("INSERT INTO reviews (book_id, user_id, rating, review) VALUES (:book_id, :user_id, :rating, :review)",
										{"book_id": book_id, "user_id": user_id, "rating": rating, "review": review})
	db.commit()

def get_book_reviews(isbn):
	book_id = get_book_id(isbn)
	
	reviews_query = db.execute("SELECT * FROM reviews WHERE book_id = :book_id", {"book_id": book_id}).fetchall()

	if reviews_query == []:
		return None
	
	reviews = []
	for review in reviews_query:
		reviews.append({
				"id": review.id,
				"reviewer_name": get_user_fullname(review.username),
				"rating": review.rating,
				"review_body": review.review,
				"pub_date": f"{review.pub_date.year}/{review.pub_date.month}/{review.pub_date.day}"
			})

	return reviews

def get_user_review(isbn, username):
	"""
	Returns review(the first one) made by username to book(based on isbn).
	Returns None if username hasn't submitted any reviews to this particular book.
	"""

	book_id = get_book_id(isbn)
	user_id = get_user_id(username)

	return db.execute("SELECT * FROM reviews WHERE (book_id = :book_id) AND (user_id = :user_id) LIMIT 1",
													{"book_id": book_id, "user_id": user_id}).fetchone()