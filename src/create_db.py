import os
import pandas as pd
from sqlalchemy import create_engine

def main():
    input_path = os.path.join("data", "processed", "books_enriched.csv")
    db_path = "books.db"
    engine = create_engine(f"sqlite:///{db_path}")
    df = pd.read_csv(input_path)
    df.to_sql("books", engine, if_exists="replace", index=False)

    print(" Baza napravljena:", db_path)
    print(" Tablica 'books' popunjena s redaka:", len(df))

if __name__ == "__main__":
    main()