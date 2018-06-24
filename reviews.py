from DB import *

#-----------------------------------------------------------------------------------------------------------------------

def add_review(isbn, user_id, rating, review):
	book_id = get_book_id(isbn)

	db.execute("INSERT INTO reviews (book_id, user_id, rating, review) VALUES (:book_id, :user_id, :rating, :review)",
		                                 {"book_id": book_id, "user_id": user_id, "rating": rating, "review": review})
	db.commit()

def get_book_reviews(isbn):
	return [{
				"reviewer_name": "Hyuri Pimentel",
				"rating": 3,
				"review_body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
			}]