![image](https://user-images.githubusercontent.com/18584014/62816963-40542e00-bb05-11e9-83c2-b4a42fc6882a.png)
![image](https://user-images.githubusercontent.com/18584014/62816990-b2c50e00-bb05-11e9-8469-1a50eb422ed2.png)
![image](https://user-images.githubusercontent.com/18584014/62817006-f3bd2280-bb05-11e9-90fb-8993409c79c4.png)

# Project 1

Web Programming with Python and JavaScript (Harvard's CS50)

#### About
Bookviews -- A book review website written in Flask/Python3, HTML5, Sass/CSS3, Bootstrap4 and JavaScript. Users are able to register, log in, search for books or authors, leave reviews for individual books, and see the reviews made by other people. It uses the third-party APIs by Goodreads for book info and ratings, OpenLibrary Covers for book covers, and Google Books for book descriptions.
It also provides an API for querying book details by ISBN`("/book/<isbn>")`.

#### master_layout.html:
Contains the base structure, layout, stylesheets and scripts, shared by every page on the website.
It has Jinja "blocks" for adding additional(named by me as "local") stylesheets and scripts, as required by each page.

#### common_header.html:
Contains just the code for the header of all the pages that share this common header in the website(the home page contains a different header). This header is included using Jinja's "include" statement.
In the header, there is the brand(name of the website), a search bar, and the username dropdown menu, which contains the "MyReviews" and "Logout" items. Clicking on "MyReviews", redirects you to a page containing all the books that this particular user has reviewed, each book linking directly(scrolling) to that user's specific review. Clicking on "Logout" terminates the user session, causing a redirection to index.

#### index.html:
Contains both a registration and a login form.

The look of the forms' container was made to resemble an open book.

#### home.html:
Contains a search bar on the center of the screen. It also has a header, containing the logged in user's username, at the top. The code for the header is contained in the "home_header.html" file.

#### home_header.html:
Contains just the code for the header of the home page. This header is included in the home page using Jinja's "include" statement.
This header contains the username, which is a dropdown menu containing the items "MyReviews" and "Logout".

#### search_results.html:
This is a generic page. It's used in many routes: When you search on the website, this page is returned with the results of your search query; when you access the `/MyReviews` route, this page is returned with a list of books that the currently-logged in user has reviewed; this page also returns all the books of a particular author, when you visit the route `/<author_name>`, or all the books published in a particular year, when you visit the route `/<year>`.
You can search for authors too and, if your search term appears both in the authors and the books tables, both authors and books will appear on the search_results page--authors first.
Putting "my reviews", "My Reviews", "MyReviews", "myreviews" or any combination of uppercase and lowercase, with or without a space in between "my" and "reviews", redirects you to the "/MyReviews" route.

#### book.html:
Contains: a "large" cover of the book(provided by OpenLibrary's Cover API); the title of the book; ratings from Bookviews and from Goodreads; the name of the author of the book(which links you to a page containing all of the books written by that author); the year of publication(which links you to a page containing all of the books written in that year); the ISBN string of the book; a description of the book(provided by Google Books API); a button indicating whether the user has already reviewed the book or not(if they have, clicking on the button scrolls to their review of the book), and a list of all the reviews for the book.

#### review_submission.html:
Contains reduced book info, and the review submission form. You should provide a rating, in stars(0-5), and a piece of text. Zero for the rating is acceptable.
Both are mandatory, and the form will not be submited if you leave empty any of these fields.

#### error_404.html:
Contains a humorous(to me) "404"/"not found" message themed around books.

#### error.html:
Contains a more generic template for errors. Not yet being used.

#### Additional Info:
- Search is pretty slow right now. Mainly--it seems--because of the limits imposed by the APIs that were used, particularly Goodreads' and, to a lesser extent, OpenLibrary's API. When there are a lot of results, you'll be waiting several seconds(probably 3-5 seconds per book). I didn't try to optimize this in any way because it was beyond the scope of this project--and I was required to use these APIs anyway;
- I've broken most of the functionality down into their own specific Python files: DB.py, books.py, reviews.py, users.py;
- I've implemented the registration & login system using "argon2", through "passlib";
- I used Sass' "Sass" syntax instead of the "Scss" one;
- I used a modified version of the "rater-js" star rating system. The modification I made was to allow setting the rating value to "undefined", which allowed me to set the rating to "undefined" when loading the page so I could check if the user had chosen a rating(0-5) or not when clicking on the "submit" button, as choosing a rating was mandatory and I didn't wanted to put "zero" as the default value because I wanted the user to explicitly choose a value. This change was later accepted by the original author and is now included upstream.
