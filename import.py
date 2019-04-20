import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


#-----------------------------------------------------------------------------

# an Engine, that the Session will use for 
# connection resources and a database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


#--- IMPORT FILE -------------------------------------------------------------
with open('books.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) " + 
                   "VALUES (:isbn, :title, :author, :year)",
                   {"isbn": row["isbn"], "title": row["title"], 
                    "author": row["author"], "year": row["year"]})
        print(f"Added book with ISBN {row['isbn']}.")
    db.commit()



