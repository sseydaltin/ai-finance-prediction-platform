"""
data/raw/ klasöründeki tüm kripto CSV dosyalarını birleştirir
ve data/raw/crypto_prices.csv olarak kaydeder.

Kullanım:
    python src/merge_raw.py          (proje kök dizininden)
"""

from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
OUTPUT_FILE = RAW_DIR / "crypto_prices.csv"


def merge_raw_csvs() -> pd.DataFrame:
    csv_files = sorted(
        f for f in RAW_DIR.glob("*.csv")
        if f.name != "crypto_prices.csv"
    )

    if not csv_files:
        raise FileNotFoundError(f"'{RAW_DIR}' klasöründe CSV dosyası bulunamadı.")

    frames = []
    for path in csv_files:
        ticker = path.stem          # "BTC.csv" → "BTC"
        df = pd.read_csv(path)

        # ticker sütunu yoksa dosya adından ekle
        if "ticker" not in df.columns:
            df.insert(0, "ticker", ticker)

        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    # date sütununu datetime'a çevir ve tarihe göre sırala
    combined["date"] = pd.to_datetime(combined["date"])
    combined.sort_values(["ticker", "date"], inplace=True)
    combined.reset_index(drop=True, inplace=True)

    return combined, len(csv_files)


def main():
    combined, n_files = merge_raw_csvs()

    combined.to_csv(OUTPUT_FILE, index=False)

    print(f"Okunan dosya sayisi : {n_files}")
    print(f"Toplam satir sayisi : {len(combined):,}")
    print(f"Benzersiz ticker    : {combined['ticker'].nunique()}")
    print(f"Kayit edildi        : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
