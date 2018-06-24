from DB import *

#-----------------------------------------------------------------------------------------------------------------------

# Fake User (temp)
class User:
	def __init__(self, user_id, name, username, password):
		self.user_id = user_id
		self.name = name
		self.username = username
		self.password = password

def get_user_id(username):
	"""
	Returns id number that matches username.
	Returns None if no matches found
	"""

	user_id = db.execute("SELECT id FROM users WHERE username = :username LIMIT 1", {"username": username}).fetchone()
	
	if user_id is None:
		return None

	return user_id[0]

def get_user_fullname(user_id):
	"""
	Returns fullname that matches user_id.
	Returns None if no matches found
	"""

	user_fullname = db.execute("SELECT fullname FROM users WHERE id = :user_id LIMIT 1", {"user_id": user_id}).fetchone()
	
	if user_fullname is None:
		return None

	return user_fullname[0]

def get_book_id(isbn):
	"""
	Returns id number that matches isbn.
	Returns None if no matches found
	"""
	book_id = db.execute("SELECT id FROM books WHERE isbn = :isbn LIMIT 1", {"isbn": isbn}).fetchone()

	if book_id is None:
		return None

	return book_id[0]