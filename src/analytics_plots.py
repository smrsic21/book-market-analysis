import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def main():
    engine = create_engine("sqlite:///books.db")
    df = pd.read_sql("SELECT * FROM books", engine)
    df_valid = df.dropna(subset=["gb_avgRating"])
    out_dir = os.path.join("docs", "figures")
    os.makedirs(out_dir, exist_ok=True)

    # 1) Price vs avgRating
    plt.figure()
    plt.scatter(df_valid["Price"], df_valid["gb_avgRating"])
    plt.xlabel("Price ($)")
    plt.ylabel("Google average rating")
    plt.title("Price vs Google average rating")
    plt.savefig(os.path.join(out_dir, "price_vs_rating.png"))
    plt.close()

    # 2) Price vs ratingsCount
    df_valid2 = df.dropna(subset=["gb_ratingsCount"])
    plt.figure()
    plt.scatter(df_valid2["Price"], df_valid2["gb_ratingsCount"])
    plt.xlabel("Price ($)")
    plt.ylabel("Google ratings count")
    plt.title("Price vs Number of ratings")
    plt.savefig(os.path.join(out_dir, "price_vs_ratingscount.png"))
    plt.close()

    # 3) Avg rating by Genre
    genre_stats = df_valid.groupby("Genre")["gb_avgRating"].mean().sort_values(ascending=False)
    plt.figure()
    genre_stats.plot(kind="bar")
    plt.xlabel("Genre")
    plt.ylabel("Average Google rating")
    plt.title("Average rating by Genre")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "avg_rating_by_genre.png"))
    plt.close()

    # 4) Trend avg rating by Year
    year_stats = df_valid.groupby("Year")["gb_avgRating"].mean().sort_index()
    plt.figure()
    plt.plot(year_stats.index, year_stats.values)
    plt.xlabel("Year")
    plt.ylabel("Average Google rating")
    plt.title("Average rating trend over years")
    plt.savefig(os.path.join(out_dir, "avg_rating_trend_year.png"))
    plt.close()

    print(" Grafovi spremljeni u:", out_dir)
    print(" Files:")
    for f in os.listdir(out_dir):
        print(" -", f)

if __name__ == "__main__":
    main()