import os
import pandas as pd


def main():
    # Putanje
    input_path = os.path.join("data", "amazon_top_50.csv")
    output_dir = os.path.join("data", "processed")
    output_path = os.path.join(output_dir, "amazon_top50_clean.csv")

    # Provjera da processed folder postoji
    os.makedirs(output_dir, exist_ok=True)

    # 1) Učitavanje CSV-a
    df = pd.read_csv(input_path)

    print(" Učitano redaka:", len(df))
    print(" Stupci:", list(df.columns))

    # 2) Osnovno čišćenje naziva stupaca (makni leading/trailing razmake)
    df.columns = [c.strip() for c in df.columns]

    # 3) Makni duplikate (isti Name + Author + Year)
    df_before = len(df)
    df = df.drop_duplicates(subset=["Name", "Author", "Year"])
    print(f" Duplikati maknuti: {df_before - len(df)}")

    # 4) Pretvori tipove podataka u ispravne
    # (ako se negdje pojavi greška u podacima, pretvorit će u NaN)
    df["User Rating"] = pd.to_numeric(df["User Rating"], errors="coerce")
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

    # 5) Normaliziraj tekst 
    df["Name"] = df["Name"].astype(str).str.strip()
    df["Author"] = df["Author"].astype(str).str.strip()
    df["Genre"] = df["Genre"].astype(str).str.strip()

    # 6) Makni redove gdje fali ključna stvar 
    df = df.dropna(subset=["Name", "Author", "Year"])

    # 7) Dodaj svoj ID 
    df = df.reset_index(drop=True)
    df.insert(0, "id", df.index + 1)

    # 8) Spremi clean dataset
    df.to_csv(output_path, index=False)
    print(" Clean dataset spremljen u:", output_path)

    # 9) Brzi pregled 
    print("\n Preview:")
    print(df.head())


if __name__ == "__main__":
    main()
