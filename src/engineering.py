import pandas as pd
import numpy as np


def add_lag_features(df: pd.DataFrame,
                     lags: list = [1, 2, 3, 5, 7]) -> pd.DataFrame:
    """
    close fiyatı için gecikme (lag) değişkenleri ekler.
    - Her lag için df["close"].shift(lag) kullan
    - Sütun adları: close_lag_1, close_lag_2, close_lag_3, ...
    """
    # TODO: lags listesi üzerinde döngü kur
    # TODO: df["close"].shift(lag) ile gecikme sütunu oluştur
    # TODO: f"close_lag_{lag}" adıyla df'e ekle
    # TODO: güncellenmiş df'i döndür
    pass


def add_rolling_features(df: pd.DataFrame,
                         windows: list = [5, 10, 20]) -> pd.DataFrame:
    """
    Rolling ortalama ve rolling standart sapma ekler.
    - Her pencere için close üzerinden hesapla
    - Sütun adları: rolling_mean_5, rolling_std_5, ...
    """
    # TODO: windows listesi üzerinde döngü kur
    # TODO: df["close"].rolling(w).mean() → rolling_mean_{w}
    # TODO: df["close"].rolling(w).std()  → rolling_std_{w}
    # TODO: güncellenmiş df'i döndür
    pass


def add_price_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    OHLC'den türetilen 4 ek öznitelik ekler:
    - daily_range  : high - low
    - body_size    : abs(close - open)
    - upper_shadow : high - max(open, close)
    - lower_shadow : min(open, close) - low
    """
    # TODO: daily_range = df["high"] - df["low"]
    # TODO: body_size = abs(df["close"] - df["open"])
    # TODO: upper_shadow = df["high"] - df[["open","close"]].max(axis=1)
    # TODO: lower_shadow = df[["open","close"]].min(axis=1) - df["low"]
    # TODO: dört sütunu df'e ekle ve döndür
    pass


def add_target_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    İki hedef değişken ekler:
    - direction   : int (0/1) – ertesi gün close bugünden yüksekse 1
    - daily_return: float (%) – (close_t / close_t-1 - 1) * 100
    UYARI: Bu sütunlar modele feature olarak verilmez!
    """
    # TODO: daily_return = close.pct_change() * 100
    # TODO: direction = (close.shift(-1) > close).astype(int)
    # TODO: son satır NaN olacak, dropna sonraya bırakılıyor
    # TODO: iki sütunu df'e ekle ve döndür
    pass


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tüm adımları pipeline gibi sırayla çalıştırır:
    add_all_indicators → add_lag_features → add_rolling_features
    → add_price_features → add_target_variables → dropna
    Hazır DataFrame döndürür, sütun sayısını yazdırır.
    """
    # TODO: her fonksiyonu sırayla çağır
    # TODO: en sonda df.dropna() uygula
    # TODO: final shape ve sütun listesini yazdır
    # TODO: temizlenmiş df'i döndür
    pass
