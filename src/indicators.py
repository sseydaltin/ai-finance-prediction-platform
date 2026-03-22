import pandas as pd

# NOT: Veri setinde volume sütunu YOKTUR.
# Sadece OHLC bazlı indikatörler kullanılacak.


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    RSI (Relative Strength Index) ekler.
    - pandas_ta ile hesapla: ta.rsi()
    - Sütun adı: rsi_14
    - Orijinal df'i değiştirme, kopyasını döndür
    """
    # TODO: df.copy() ile kopya oluştur
    # TODO: ta.rsi(df["close"], length=period) ile hesapla
    # TODO: sonucu f"rsi_{period}" adıyla DataFrame'e ekle
    # TODO: güncellenmiş df'i döndür
    pass


def add_macd(df: pd.DataFrame, fast: int = 12,
             slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """
    MACD, MACD_signal ve MACD_hist sütunlarını ekler.
    - pandas_ta ile hesapla: ta.macd()
    - 3 yeni sütun eklenecek: macd, macd_signal, macd_hist
    """
    # TODO: ta.macd(df["close"], fast=fast, slow=slow, signal=signal)
    # TODO: dönen DataFrame'in sütunlarını macd, macd_signal, macd_hist olarak yeniden adlandır
    # TODO: orijinal df'e ekle ve döndür
    pass


def add_bollinger_bands(df: pd.DataFrame, period: int = 20,
                        std: float = 2.0) -> pd.DataFrame:
    """
    Bollinger Bands ekler.
    - pandas_ta ile hesapla: ta.bbands()
    - Sütun adları: bb_upper, bb_mid, bb_lower
    """
    # TODO: ta.bbands(df["close"], length=period, std=std) ile hesapla
    # TODO: sütunları bb_upper, bb_mid, bb_lower olarak yeniden adlandır
    # TODO: orijinal df'e ekle ve döndür
    pass


def add_ema(df: pd.DataFrame,
            periods: list = [7, 14, 21, 50]) -> pd.DataFrame:
    """
    Birden fazla periyot için EMA ekler.
    - Her periyot için ta.ema() çağır
    - Sütun adları: ema_7, ema_14, ema_21, ema_50
    """
    # TODO: periods listesi üzerinde döngü kur
    # TODO: her periyot için ta.ema(df["close"], length=p) hesapla
    # TODO: f"ema_{p}" adıyla df'e ekle
    # TODO: güncellenmiş df'i döndür
    pass


def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    ATR (Average True Range) ekler.
    - High, Low, Close kullanır – volume gerekmez
    - pandas_ta ile hesapla: ta.atr()
    - Sütun adı: atr_14
    """
    # TODO: ta.atr(df["high"], df["low"], df["close"], length=period)
    # TODO: sonucu f"atr_{period}" adıyla ekle ve döndür
    pass


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tüm indikatör fonksiyonlarını sırayla çağırır.
    Sıra: add_rsi → add_macd → add_bollinger_bands → add_ema → add_atr
    NOT: NaN temizliği burada yapılmaz, engineering.py'de yapılacak.
    """
    # TODO: her fonksiyonu sırayla çağır, df'i güncelle
    # TODO: son df'i döndür
    pass
