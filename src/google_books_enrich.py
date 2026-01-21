import os
import time
import requests
import pandas as pd


def fetch_google_books_data(title: str, author: str):
    """
    Dohvati podatke s Google Books API-ja za zadani naslov i autora.
    Vraća dict s poljima koje želimo ili None vrijednosti ako nema rezultata.
    """
    query = f'intitle:"{title}" inauthor:"{author}"'
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": 1}

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        if "items" not in data or len(data["items"]) == 0:
            return {
                "gb_categories": None,
                "gb_avgRating": None,
                "gb_ratingsCount": None,
                "gb_publisher": None,
                "gb_publishedDate": None,
                "gb_pageCount": None,
                "gb_language": None,
            }

        volume = data["items"][0].get("volumeInfo", {})

        categories = volume.get("categories")
        if isinstance(categories, list):
            categories = ", ".join(categories)

        return {
            "gb_categories": categories,
            "gb_avgRating": volume.get("averageRating"),
            "gb_ratingsCount": volume.get("ratingsCount"),
            "gb_publisher": volume.get("publisher"),
            "gb_publishedDate": volume.get("publishedDate"),
            "gb_pageCount": volume.get("pageCount"),
            "gb_language": volume.get("language"),
        }

    except Exception as e:
        print(f" Greška za '{title}' ({author}): {e}")
        return {
            "gb_categories": None,
            "gb_avgRating": None,
            "gb_ratingsCount": None,
            "gb_publisher": None,
            "gb_publishedDate": None,
            "gb_pageCount": None,
            "gb_language": None,
        }


def main():
    input_path = os.path.join("data", "processed", "amazon_top50_clean.csv")
    output_path = os.path.join("data", "processed", "books_enriched.csv")

    df = pd.read_csv(input_path)

    enriched_rows = []

    print(" Krećem dohvat s Google Books API-ja...")
    for i, row in df.iterrows():
        title = row["Name"]
        author = row["Author"]

        gb_data = fetch_google_books_data(title, author)

        combined = row.to_dict()
        combined.update(gb_data)
        enriched_rows.append(combined)

        # mali delay da ne spamamo API
        if (i + 1) % 20 == 0:
            print(f" Odrađeno {i+1}/{len(df)} knjiga...")
        time.sleep(0.2)

    enriched_df = pd.DataFrame(enriched_rows)
    enriched_df.to_csv(output_path, index=False)

    print(" Gotovo! Enriched dataset spremljen u:", output_path)
    print(enriched_df.head())


if __name__ == "__main__":
    main()
