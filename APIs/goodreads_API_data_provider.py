from APIs import api_data_provider
API_data_provider = api_data_provider.API_data_provider

import requests


#class to display the average rating and number of ratings the work has 
#received on Goodreads (if available) - extends the API_data_provider interface
class Goodreads_API_data_provider(API_data_provider):
    def get_API_Data_json(self, isbn: str) -> str:
        # getting data from the Goodreads API
        response = requests.get(
            "https://www.goodreads.com/book/review_counts.json", 
            params={"key": "igKPxB8mfFqrN2TjTUxwVw", "isbns": isbn})

        # if the request was not successful:
        if response.status_code is not 200:
            return dict(number_of_ratings="(No rating found on goodreads.com)",
                        average_rating="-")

        result = response.json()
        if len(result) is not 1:
            raise ValueError(
                "Unexpected error: the search returned more results with " + 
                "the same ISBN number")

        # Request successful, get rating data from response and return it
        return result




