from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_raw(filename: str = "crypto_prices.csv") -> pd.DataFrame:
    """
    data/raw/ klasöründeki birleşik ham CSV dosyasını okur.

    Beklenen sütunlar: ticker, date, open, high, low, close
    - date sütununu datetime formatına çevirir
    - Tarihe göre artan sırada sıralar
    - Okunan satır sayısını ve benzersiz coin sayısını yazdırır

    Parametreler
    ------------
    filename : str
        data/raw/ altındaki CSV dosyasının adı (varsayılan: crypto_prices.csv)

    Döndürür
    --------
    pd.DataFrame
    """
    filepath = RAW_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(
            f"'{filepath}' bulunamadı. Önce src/merge_raw.py çalıştırın."
        )

    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f"[load_raw] Satir sayisi     : {len(df):,}")
    print(f"[load_raw] Benzersiz coin   : {df['ticker'].nunique()}")

    return df


def get_all_tickers(df: pd.DataFrame) -> list:
    """
    DataFrame içindeki tüm benzersiz ticker'ları alfabetik sırayla döndürür.

    Parametreler
    ------------
    df : pd.DataFrame
        ticker sütunu içeren ham veya filtrelenmiş DataFrame

    Döndürür
    --------
    list[str]
        Sıralı ticker listesi (örn. ['BTC', 'ETH', 'LTC', ...])
    """
    tickers = sorted(df["ticker"].unique().tolist())
    print(f"[get_all_tickers] Toplam coin sayisi: {len(tickers)}")
    return tickers


def filter_coin(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Birleşik DataFrame'den tek bir coin'e ait satırları filtreler.

    - Belirtilen ticker'a göre filtreler
    - date sütununu index olarak ayarlar
    - Satır sayısını ve tarih aralığını yazdırır

    Parametreler
    ------------
    df     : pd.DataFrame  Ham veya filtrelenmiş DataFrame
    ticker : str           Coin sembolü (örn. 'BTC')

    Döndürür
    --------
    pd.DataFrame
        date sütunu index olarak ayarlanmış, tek coin DataFrame'i

    Raises
    ------
    ValueError
        ticker DataFrame'de bulunamazsa
    """
    if ticker not in df["ticker"].values:
        mevcut = sorted(df["ticker"].unique())
        raise ValueError(
            f"'{ticker}' bulunamadı. Mevcut ticker'lar: {mevcut}"
        )

    coin_df = df[df["ticker"] == ticker].copy()
    coin_df = coin_df.drop(columns=["ticker"])
    coin_df = coin_df.set_index("date")
    coin_df.sort_index(inplace=True)

    print(
        f"[filter_coin] {ticker} -> {len(coin_df):,} satir  "
        f"| {coin_df.index.min().date()} / {coin_df.index.max().date()}"
    )

    return coin_df


def check_data_quality(df: pd.DataFrame, min_rows: int = 365) -> pd.DataFrame:
    """
    Her coin için veri yeterliliğini kontrol eder; yetersiz coinleri eler.

    - min_rows'dan az satırı olan coinlerin tüm satırlarını siler
    - Elenen ve kalan coin sayısını yazdırır

    Parametreler
    ------------
    df       : pd.DataFrame  Ham DataFrame (ticker sütunu içermeli)
    min_rows : int           Bir coin için kabul edilebilir minimum satır sayısı

    Döndürür
    --------
    pd.DataFrame
        Yalnızca yeterli veriye sahip coinleri içeren DataFrame
    """
    coin_counts = df.groupby("ticker").size()

    yetersiz = coin_counts[coin_counts < min_rows].index.tolist()
    yeterli = coin_counts[coin_counts >= min_rows].index.tolist()

    if yetersiz:
        print(f"[check_data_quality] Elenen  ({len(yetersiz)} coin, <{min_rows} satir): "
              f"{sorted(yetersiz)}")
    print(f"[check_data_quality] Kalan   : {len(yeterli)} coin  (min {min_rows} satir)")

    return df[df["ticker"].isin(yeterli)].copy().reset_index(drop=True)


def load_filtered(
    filename: str = "crypto_prices.csv",
    min_rows: int = 365,
) -> pd.DataFrame:
    """
    Ham CSV'yi okur, veri kalitesi filtresini uygular ve temizlenmiş
    DataFrame döndürür.

    Diğer modüller (indicators.py, engineering.py, models.py) ham veri
    yerine bu fonksiyonu kullanmalıdır.

    Parametreler
    ------------
    filename : str  data/raw/ altındaki CSV dosyası
    min_rows : int  Coin başına minimum satır eşiği (varsayılan: 365)

    Döndürür
    --------
    pd.DataFrame
        Kalite filtresinden geçmiş, date sıralamalı DataFrame
    """
    df = load_raw(filename)
    df = check_data_quality(df, min_rows=min_rows)
    return df


if __name__ == "__main__":
    df = load_filtered()
    tickers = get_all_tickers(df)
    print(f"Kullanilacak coin sayisi: {len(tickers)}")
