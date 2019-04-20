import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash


# ---SETTING UP DATABASE------------------------------------------------------

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# ---USER CLASS---------------------------------------------------------------

class User:
    
    def __init__(self, user_name):
        self.username = user_name


    # ---METHOD DEFINITIONS---------------------------------------------------

    def check_login_data(self, password):
        # searching for username in db, checking if it is there
        user_data = db.execute("SELECT * FROM users WHERE user_name = :un", 
                               {"un": self.username}).fetchone()
        if user_data is None:
            return "Sorry, it seems you put in a username that we cannot find in our database."

        if check_password_hash(user_data.password, password) == False:
            return "Sorry, it seems you did not put in the correct password."

        # if all data checks out, return no error message
        return None


    def register(self, password, password2):
        # checking registration input data
        error_in_reg_validation_message = self.validate_reg_input(
                                               password, password2)
        if error_in_reg_validation_message:
            return error_in_reg_validation_message

        if self.is_username_duplicate_in(db):
            return "Sorry, this username is already taken:( Please choose another one."

        # if everything was OK, save the registration data
        # into the database and return no error message
        self.save_user_data_in_database(password, password2)
        return None


    def validate_reg_input(self, password, password2):
        # this can happen since the user object was initialized
        # with the username input of the registration form
        if self.username == "":
            return "Please provide a user name."

        if password == "":
            return "Please provide a password."

        if password2 == "":
            return "Please repeat your password."

        if not password == password2:
            return "The two passwords given don't match. Please try again."

        # No error message means the input is valid and can be saved to db.
        return None


    def is_username_duplicate_in(self, db):
        if db.execute("SELECT * FROM users WHERE user_name = :un", 
                      {"un": self.username}).rowcount == 0:
            return False

        return True


    def save_user_data_in_database(self, password, password2):
        # Encrypting password
        pw = generate_password_hash(password)

        # Saving data in database
        db.execute("INSERT INTO users (user_name, password) " + 
                   "VALUES (:username, :password)",
                  {"username": self.username, "password": pw})
        db.commit()