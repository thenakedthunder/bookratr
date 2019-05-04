import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# ---SETTING UP DATABASE------------------------------------------------------

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# ---BOOK CLASS---------------------------------------------------------------

class Book:
    
    def __init__(self, book_data, reviews):
        self.isbn =  book_data['isbn']
        self.title = book_data['title']
        self.author = book_data['author'] 
        self.year = book_data['year']
        self.reviews = reviews


    # ---METHOD DEFINITIONS---------------------------------------------------

    # return the user's review of the book if there is one
    def get_review_by_user(self, username):
        # filter reviews by the username
        reviews_by_user = list(filter(
            lambda review: review['user_name'] == username, self.reviews))
        
        reviews_count = len(reviews_by_user)
        if reviews_count > 1:
            # throwing exception because this method is called from code
            raise ValueError("Unexpected error: this user has reviewed " +
                             "this book more than once.")
        if reviews_count == 1:
            return reviews_by_user[0]
        
        return None


    # gets the average of the ratings given to this book
    def get_average_score(self):
        if len(self.reviews) is 0:
            return 0

        # fetching a collection of ratings from the reviews collection
        ratings = [review['rating'] for review in self.reviews]

        result = sum(ratings) / len(ratings)
        return round(result, 2)


    # region Static Methods

    # Searches for a book by data given by user in the search form
    @staticmethod
    def search(isbn, title, author):
        # check if user has given enough search data
        if (isbn == "" and title == "" and author == ""):
            return "Please put in at least a fraction of the ISBN, title or author."

        # check books that match in db
        results = db.execute("SELECT author, title FROM books " + 
                             "WHERE UPPER(isbn) LIKE :isbn " + 
                             "AND UPPER(title) LIKE :title " + 
                             "AND UPPER(author) LIKE :author", 
                             {"isbn": '%' + isbn.upper() + '%', 
                              "title": '%' + title.upper() + '%', 
                              "author": '%' + author.upper() + '%'}).fetchall()
        
        if len(results) == 0:
            return "No book found. Please try the search over with different search criteria."

        return results


    # Returns book by the given isbn number
    @staticmethod
    def search_by(isbn):
        results = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn ", 
                             {"isbn": isbn}).fetchall()
        
        results_count = len(results)
        if results_count < 1:
            return "The search found no book."
        if results_count > 1:
            raise "Error: The search found more than one book."

        return results[0]


    @staticmethod
    def get_book_author_and_title_by(isbn):
        if (isbn == ""):
            # throwing exception because this method is called from code
            raise ValueError("Unexpected error: no ISBN number.")

        # find the book that matches in db
        results = db.execute("SELECT author, title FROM books " + 
                             "WHERE isbn LIKE :isbn ", 
                             {"isbn": isbn}).fetchall()
        
        if len(results) != 1:
            # throwing exception because this method is called from code
            raise ValueError(
                "Unexpected error: less or more than one result for search.")

        result = results[0]['author'] + ":" + results[0]['title']
        # replace needed because spaces are not allowed in links
        return result.replace(' ', '_')


    @staticmethod
    def search_from_string_composed_by(book_author_and_title):
        if (book_author_and_title == "" or book_author_and_title is None):
            # throwing exception because this method is called from code
            raise ValueError(
                "Unexpected error: the title and author not given.")

        # building the search terms from the link format and search
        author, title = book_author_and_title.replace("_", " ").split(":")
        results = db.execute("SELECT * FROM books " + 
                             "WHERE title =:title AND author =:author", 
                             {"title": title, "author": author}).fetchall()
        # The search was made by title and author, 
        # so the number of results should be exactly one
        if len(results) != 1:
            raise ValueError("Unexpected error: The search returned no or " +
                             "more than one result.")

        return results[0]

    # endregion
  




