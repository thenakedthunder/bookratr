# Project 1

Web Programming with Python and JavaScript

------------------------------------------

This is a pet project based on project1 of the CS50W course. More details on this course: 
https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript

You can get to know about the project itself after signing up here: 
https://docs.cs50.net/web/2018/x/projects/1/project1.html
However, if you want to have a look at the feature specification, I kindly included that in specs.txt.
I also uploaded too images with the class diagram, if you like the visual presentation better. One
is an "overwhelming" version showing all the dependencies, the other is purer and therefore easier 
to comprehend.

I INTENTIONALLY OMITTED THE USE OF JAVASCRIPT because of said requirements. I know that the use of
it could have made the whole site and code better. For checking on my JS skills, please take a look
at the other project on this repo.

The whole code here is my own work, the only assistance I got was from virtual "partners" like 
Google and Stack Overflow. The only code parts I did NOT write were for the part where users can 
rate the books: here, the html and css code for displaying golden stars instead of radio buttons is
a solution I copied from somewhere on the internet. This is also true for the star images. 
Unfortunately, I forgot to write the name of the source down, so I am not able to mention it now. 
However, in the code in book.html, I marked the places where I use this "borrowed" code.

------------------------------------------- COMPONENTS: -------------------------------------------

--------------------------------------------- Clients ---------------------------------------------

APPLICATION 

application.py:
This class runs the show. It is the entry point of the whole application (save import.py, which is 
a standalone tool separated from everything else.) Using the other classes and their methods, this
one is responsible for all routings and request handlings. Any client SHOULD access the application
through this class.

APIs

api_data_provider: 
provides an interface that has to be used to serve API-related information requests. By this
restriction, future extension or modification of the current API provider classes is made easier.
The interface ensures that an input isbn number will yield a json containing the provided book data.

goodreads_API_data_provider:
Gets data from a Goodreads API and returns the average rating and number of ratings the work has 
received there (if available) - the class extends the API_data_provider interface

bookratr_API_data_provider:
Gathers data provided by the application's own API (isbn, author and title of book, the year it was
written, the number of reviews and the average rating it got.) The class extends the 
API_data_provider interface


------------------------------------------- Data Access -------------------------------------------

This component does not only function as a persistance layer. In order to avoid making the 
application too complicated to understand, business logic built upon the persistance access methods
is also places in these classes. This is not SOLID, however, for such a small application, that is 
not likely to scale up in the near future, this is an intended and understood tradeoff.

user.py:
Contains methods for handling user logins and registration. It has two open functions meant to be
used from the outside, while the rest is the inside implementation of the business logic for them.

book.py:
This knows of and uses the implementation of the Review object, since one book can have many 
reviews. Therefore, at instantiation an iterable of reviews has to be passed to the constructor.
Also needed here is a dict that has info for the isbn, author, title and year (each in strings).
Two methods from here handle the reviews (returning the review of the user by a given username and
a calculation of the average rating of the book, respectively), while the others are static methods
serving the clients' persistence access needs.

review.py:
Gets data needed for storing a review (constructor). Clients can use it to save these into 
persistence (public method) or to obtain reviews (static function).

--------------------------------------- Tools and Utilities ---------------------------------------

import.py:
This part is completely separated from the rest of the application, as it runs independently from
the command line. It takes a csv file (that one can create in Excel, for example), and imports book
data from there. The current implementation requires that this file is called books.csv, but that 
can easily be modified in the file, even by making this name a command line argument. This 
implementation is due to the requirements (see specs.txt for more info on that.)

utility.py:
As the name suggests, this class is for static utility methods used in the application.
