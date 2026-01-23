import os
import pandas as pd

def main():
    input_path = os.path.join("data", "amazon_top_50.csv")
    output_dir = os.path.join("data", "processed")
    output_path = os.path.join(output_dir, "amazon_top50_clean.csv")
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(input_path)

    print(" Učitano redaka:", len(df))
    print(" Stupci:", list(df.columns))

    df.columns = [c.strip() for c in df.columns]

    df_before = len(df)
    df = df.drop_duplicates(subset=["Name", "Author", "Year"])
    print(f" Duplikati maknuti: {df_before - len(df)}")

    df["User Rating"] = pd.to_numeric(df["User Rating"], errors="coerce")
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

    df["Name"] = df["Name"].astype(str).str.strip()
    df["Author"] = df["Author"].astype(str).str.strip()
    df["Genre"] = df["Genre"].astype(str).str.strip()

    df = df.dropna(subset=["Name", "Author", "Year"])
    df = df.reset_index(drop=True)
    df.insert(0, "id", df.index + 1)

    df.to_csv(output_path, index=False)
    print(" Clean dataset spremljen u:", output_path)
    print("\n Preview:")
    print(df.head())

if __name__ == "__main__":
    main()