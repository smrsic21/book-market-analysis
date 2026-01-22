from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

# konekcija na SQLite bazu
engine = create_engine("sqlite:///books.db")


@app.route("/")
def home():
    return jsonify({
        "message": "Book Market Analysis API is running",
        "endpoints": [
            "/books",
            "/books/<id>",
            "/analytics/price-vs-rating",
            "/analytics/genre-stats"
        ]
    })


#  1) SVE KNJIGE 
@app.route("/books", methods=["GET"])
def get_books():
    year = request.args.get("year")   
    genre = request.args.get("genre")  
    limit = request.args.get("limit", default=50, type=int)

    query = "SELECT * FROM books WHERE 1=1"
    params = {}

    if year:
        query += " AND Year = :year"
        params["year"] = int(year)

    if genre:
        query += " AND Genre = :genre"
        params["genre"] = genre

    query += " LIMIT :limit"
    params["limit"] = limit

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        rows = [dict(r._mapping) for r in result]

    return jsonify(rows)


#  2) JEDNA KNJIGA PO ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    query = "SELECT * FROM books WHERE id = :id"

    with engine.connect() as conn:
        result = conn.execute(text(query), {"id": book_id}).fetchone()

    if result is None:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(dict(result._mapping))


#  3) ANALITIKA: cijena vs ocjena (Google rating)
@app.route("/analytics/price-vs-rating", methods=["GET"])
def price_vs_rating():
    query = """
    SELECT Name, Author, Price, gb_avgRating, gb_ratingsCount
    FROM books
    WHERE gb_avgRating IS NOT NULL
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = [dict(r._mapping) for r in result]

    return jsonify(rows)


#  4) ANALITIKA: prosječna ocjena po žanru
@app.route("/analytics/genre-stats", methods=["GET"])
def genre_stats():
    query = """
    SELECT Genre,
           COUNT(*) as num_books,
           AVG(Price) as avg_price,
           AVG(gb_avgRating) as avg_rating
    FROM books
    GROUP BY Genre
    """

    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = [dict(r._mapping) for r in result]

    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
