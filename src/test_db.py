from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///books.db")
df = pd.read_sql("SELECT Name, Author, Price, gb_avgRating, gb_ratingsCount FROM books LIMIT 5", engine)
print(df)