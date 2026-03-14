import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

# Projede kullanılacak coinler – ekip buradan değiştirebilir
COINS = ["BTC", "ETH", "LTC", "XRP"]


def load_raw(filename: str = "crypto_prices.csv") -> pd.DataFrame:
    """
    data/raw/ klasöründeki ham Kaggle CSV dosyasını okur.
    Beklenen sütunlar: ticker, date, open, high, low, close
    - date sütununu datetime formatına çevir
    - Tarihe göre sırala
    - Okunan satır sayısını ve benzersiz ticker sayısını yazdır
    """
    # TODO: pd.read_csv ile dosyayı oku
    # TODO: date sütununu pd.to_datetime ile dönüştür
    # TODO: date sütununa göre sort_values uygula
    # TODO: satır sayısı ve ticker sayısını print ile yazdır
    pass


def filter_coin(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Ham DataFrame'den belirtilen ticker satırlarını filtreler.
    - ticker sütununa göre filtrele
    - date sütununu index olarak ayarla
    - Bulunan satır sayısını ve tarih aralığını yazdır
    """
    # TODO: df[df["ticker"] == ticker] ile filtrele
    # TODO: set_index("date") uygula
    # TODO: satır sayısı ve min/max tarihi yazdır
    pass


def check_coins(df: pd.DataFrame) -> None:
    """
    COINS listesindeki her coin için:
    - Kaç satır var
    - Başlangıç ve bitiş tarihi nedir
    - 1000 satırdan az varsa uyarı ver
    """
    # TODO: COINS üzerinde döngü kur
    # TODO: her coin için satır sayısı ve tarih aralığı hesapla
    # TODO: 1000 altındaysa "UYARI: yetersiz veri" yazdır
    pass


def split_and_save(df: pd.DataFrame) -> None:
    """
    COINS listesindeki her coin için filter_coin() çağırır ve
    data/processed/{ticker}.csv olarak kaydeder.
    """
    # TODO: COINS üzerinde döngü kur
    # TODO: her coin için filter_coin() çağır
    # TODO: to_csv ile data/processed/{ticker}.csv kaydet
    # TODO: kayıt sonrası onay mesajı yazdır
    pass


def load_processed(ticker: str) -> pd.DataFrame:
    """
    data/processed/{ticker}.csv dosyasını okur ve döndürür.
    Dosya bulunamazsa anlaşılır hata mesajı ver.
    """
    # TODO: dosya yolunu oluştur
    # TODO: dosya yoksa FileNotFoundError ile açıklayıcı mesaj ver
    # TODO: pd.read_csv ile oku, date sütununu index yap
    pass


if __name__ == "__main__":
    # Bu dosya doğrudan çalıştırıldığında:
    # 1. Ham veriyi yükle
    # 2. Coin kontrolü yap
    # 3. Coin CSV'lerini oluştur
    df = load_raw()
    check_coins(df)
    split_and_save(df)
