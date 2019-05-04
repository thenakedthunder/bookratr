from data_access import book
from APIs import api_data_provider
API_data_provider = api_data_provider.API_data_provider


class Utility:
    @staticmethod
    # gets the info that is to be shown on the book details page
    def get_template_context_from(book, api_data_provider, username):
        review_by_user = book.get_review_by_user(username)
        average_rating = book.get_average_score()
        goodreads_rating_data = Utility.get_rating_data_dict(
                                    api_data_provider, book)

        return dict(book=book, user_review=review_by_user,
                    avg_rating=average_rating,
                    goodreads_rating_data = goodreads_rating_data)

    @staticmethod
    # helper method to use the api_data_provider protocol and
    # convert the json data it returns into a dictionary
    def get_rating_data_dict(api_data_provider, book):
        if not isinstance(api_data_provider, API_data_provider):
            raise TypeError("A provider that implements the " + 
                            "API_data_provider must be used")

        goodreads_json = api_data_provider.get_API_Data_json(
                                    book.isbn)["books"][0]     
        goodreads_rating_data = dict(
                number_of_ratings=goodreads_json["work_ratings_count"],
                average_rating=goodreads_json["average_rating"])

        return goodreads_rating_data