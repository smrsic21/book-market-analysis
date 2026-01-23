# book-market-analysis
Analiza tržišnog uspjeha knjiga usporedbom prodajnih rezultata i online recenzija

Cilj projekta je analizirati tržišni uspjeh knjiga povezivanjem podataka iz dva heterogena izvora:
- **Amazon Top 50 Bestselling Books (2009–2019)** dataset (CSV)
- **Google Books API** (JSON)

## Pokretanje projekta
1) Instaliraj pakete:
pip install -r requirements.txt

2) Očisti Amazon dataset:
python src/ingest_csv.py

3) Obogati podatke preko Google Books API-ja:
python src/google_books_enrich.py

4) Kreiraj SQLite bazu:
python src/create_db.py

5) (Opcionalno) Test baze:
python src/test_db.py

6) Pokreni REST API:
python src/api.py
API radi na: http://127.0.0.1:5000

7) Generiraj grafove:
python src/analytics_plots.py
