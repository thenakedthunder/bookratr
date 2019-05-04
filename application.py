import os

from flask import Flask, session, render_template, request, redirect, url_for, abort
from flask_session import Session

# own modules
from data_access import book, user, review
Book, User, Review = book.Book, user.User, review.Review

from APIs import api_data_provider, goodreads_API_data_provider, bookratr_API_data_provider
API_data_provider = api_data_provider.API_data_provider
Goodreads_API_data_provider = goodreads_API_data_provider.Goodreads_API_data_provider
Bookratr_API_data_provider = bookratr_API_data_provider.Bookratr_API_data_provider

import utility
Utility = utility.Utility

# Setting up the app ---------------------------------------------------------

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Routes ---------------------------------------------------------------------

# Rendering the search page if user is logged in
@app.route("/")
def __index():
    if "username" in session:
        return render_template("search.html")

    # else take them to the login page
    return render_template("login.html")


# Login logic
@app.route("/login", methods=["POST"])
def __login():
    # Getting user input
    user = User(request.form.get("username"))
    password = request.form.get("password")
    
    # Searching for username in db, tell the user if something was wrong
    input_validation_error_message = user.check_login_data(password)
    if input_validation_error_message:
        return render_template("login.html", 
                               message=input_validation_error_message)

    # Logging in
    session["username"] = user.username
    return redirect(url_for("__index"))


@app.route("/register", methods=["GET", "POST"])
def __register():
    if request.method == "GET":
        # tell the user that registration should not be 
        # possible if a user is logged in
        if "username" in session:
            return render_template("logout.html")

        # else take them to the register page
        return render_template("register.html")


    # else:
    # "Handling in" the registration form, POST
    user = User(request.form.get("username"))
    password = request.form.get("password")
    password2 = request.form.get("password_again")

    # check if everything is filled out, passwords match
    # and tell the user if there is a problem
    input_validation_error_message = user.register(password, password2)
    if input_validation_error_message:
        return render_template("register.html", 
                               message=input_validation_error_message)

    return redirect(url_for("__index"))

@app.route("/logout")
def __logout():
    # remove the username from the session
   session.pop("username", None)

   return redirect(url_for("__index"))

@app.route("/search", methods=["POST"])
def __search():
    # "handling in" the search form
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    
    result_of_search = Book.search(isbn, title, author)

    # The search method returns an error message string, if something 
    # goes wrong. Otherwise it returns a list of results
    if type(result_of_search) is not list:
        return render_template("search.html", message=result_of_search)

    return render_template("books.html", books=result_of_search)


@app.route("/books/<book_author_and_title>")
# Find book and its reviews in db and show these details
def __book(book_author_and_title):
    book_to_show = Book.search_from_string_composed_by(book_author_and_title)
    reviews = Review.get_reviews(book_to_show['isbn'])
    book = Book(book_to_show, reviews)

    # for easy extendibility, any custom object that corresponds with the 
    # API_data_provider protocol can be put in here. 
    api_data_provider = Goodreads_API_data_provider()

    template_context = Utility.get_template_context_from(
                        book, api_data_provider, session["username"])

    return render_template("book.html", **template_context)


@app.route("/rate/<book_isbn>", methods=["POST"])
def __rate(book_isbn):
    # Getting rating input (Rating is 4 by default, 
    # while the review text is optional)
    rating = request.form.get("rating"), 
    review_text = request.form.get("review-text")
    review = Review(rating, review_text)

    # Book details needed to render book page
    book_author_and_title = Book.get_book_author_and_title_by(book_isbn)
    
    review.save_to_database(book_isbn, session["username"])
    return redirect(url_for(
        "__book", book_author_and_title = book_author_and_title))

@app.route("/api/<isbn>")
# returns a JSON response containing the book’s title, author, 
# publication date, ISBN number, review count, and average score
def __provide_book_data(isbn):
    api_data_provider = Bookratr_API_data_provider()
    if not isinstance(api_data_provider, API_data_provider):
        raise TypeError("A provider that implements the " + 
                        "API_data_provider must be used")

    return api_data_provider.get_API_Data_json(isbn)