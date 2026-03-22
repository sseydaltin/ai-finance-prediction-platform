from pathlib import Path

import pandas as pd

# Proje kök dizini: src/ klasörünün bir üstü
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_raw(filename: str = None) -> pd.DataFrame:
    """
    data/raw/crypto_prices.csv dosyasını okur.
    Beklenen sütunlar: ticker, date, open, high, low, close
    """
    path = Path(filename) if filename else RAW_DIR / "crypto_prices.csv"
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    print(f"{len(df)} satır, {df['ticker'].nunique()} ticker yüklendi")
    return df


def get_all_tickers(df: pd.DataFrame) -> list:
    """Tüm benzersiz ticker'ları alfabetik sırada döndürür."""
    return sorted(df["ticker"].unique().tolist())


def filter_coin(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Ham DataFrame'den tek bir coinin verilerini filtreler.
    date sütununu index yapar, ticker sütununu düşürür.
    """
    coin_df = df[df["ticker"] == ticker].copy()
    coin_df = coin_df.set_index("date")
    coin_df = coin_df.drop(columns=["ticker"])
    return coin_df


def check_data_quality(df: pd.DataFrame, min_rows: int = 365) -> pd.DataFrame:
    """
    Her coin için satır sayısını kontrol eder.
    min_rows'dan az verisi olan coinleri filtreler.
    """
    counts = df.groupby("ticker").size()
    valid_tickers = counts[counts >= min_rows].index.tolist()
    filtered = df[df["ticker"].isin(valid_tickers)].copy()
    removed = len(counts) - len(valid_tickers)
    if removed > 0:
        print(f"UYARI: {removed} coin yetersiz veri nedeniyle elendi (< {min_rows} satır)")
    print(f"Kalite kontrolü geçti: {len(valid_tickers)} coin, {len(filtered)} satır")
    return filtered


def load_filtered(
    filename: str = None, min_rows: int = 365
) -> pd.DataFrame:
    """
    Ana giriş noktası. load_raw() + check_data_quality() birleşimi.
    Temizlenmiş, sıralanmış, kalite kontrollü DataFrame döndürür.
    """
    df = load_raw(filename)
    df = check_data_quality(df, min_rows)
    return df


if __name__ == "__main__":
    df = load_filtered()
    tickers = get_all_tickers(df)
    print(f"{len(tickers)} ticker yüklendi, {len(df)} satır")
