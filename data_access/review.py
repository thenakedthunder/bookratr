import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.functions import now
from datetime import datetime


# ---SETTING UP DATABASE------------------------------------------------------

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# ---REVIEW CLASS-------------------------------------------------------------

class Review:
    
    def __init__(self, rating, review_text):
       self.rating = rating
       self.review_text = review_text
       self.time_of_review = datetime.date(datetime.now())


    # ---METHOD DEFINITIONS---------------------------------------------------

    def save_to_database(self, isbn, username):
        # Saving data in database
        db.execute("INSERT INTO reviews (book_isbn, user_name, " + 
                   "time_of_review, rating, review_text) " + 
                   "VALUES (:isbn, :username, :time_of_review, :rating, " + 
                   ":reviewtext)",
                  {"isbn": isbn, "username": username, 
                   "time_of_review": self.time_of_review,
                   "rating": self.rating, "reviewtext": self.review_text})
        db.commit()


    # ---STATIC METHODS-------------------------------------------------------

    @staticmethod
    # getting reviews of the book with given isbn    
    def get_reviews(isbn):
        reviews = db.execute("SELECT user_name, " + 
                             "to_char(time_of_review, :time_expression) " + 
                             "AS time_of_review, rating, review_text " + 
                             "FROM reviews " +
                             "WHERE book_isbn = :isbn",
                             {"time_expression": 'Month DD, YYYY',
                              "isbn": isbn}).fetchall()

        return reviews