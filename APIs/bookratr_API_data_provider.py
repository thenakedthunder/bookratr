import json
from flask import abort

# own modules
from APIs import api_data_provider
API_data_provider = api_data_provider.API_data_provider

from data_access import book, review
Book, Review = book.Book, review.Review

# returns a JSON response containing the book’s title, author, 
# publication date, ISBN number, review count, and average score
class Bookratr_API_data_provider(API_data_provider):
    def get_API_Data_json(self, isbn: str) -> str:
        result_of_search = Book.search_by(isbn)

        # The search method returns a list of results, if the search 
        # ran and found EXACTLY ONE result. If not, return with 404
        if type(result_of_search) is str:
            abort(404)
    
        reviews = Review.get_reviews(result_of_search['isbn'])
        book = Book(result_of_search, reviews)
        
        data = dict(title=book.title, author=book.author, year=book.year,
                    isbn=book.isbn)
        data['review_count'] = len(reviews)
        data['average_score'] = book.get_average_score()

        json_data = json.dumps(data)
        return json_data