"""
Teknik indikatör hesaplama modülü.

Kural: Tüm fonksiyonlar date-index'li, ticker sütunu olmayan
tek bir coin DataFrame'i alır ve yeni sütunlar eklenmiş kopyasını döndürür.
NaN temizliği bu modülde yapılmaz; engineering.py'de tek seferinde uygulanır.
"""

import pandas as pd
import pandas_ta as ta


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Relative Strength Index (RSI) hesaplar ve DataFrame'e ekler.

    Parametreler
    ------------
    df     : pd.DataFrame  En az 'close' sütunu olan coin verisi
    period : int           RSI pencere uzunlugu (varsayilan: 14)

    Eklenen sutun
    -------------
    rsi_14 : float  0-100 araliginda momentum gostergesi

    Döndürür
    --------
    pd.DataFrame  Orijinal verinin degistirilmemis kopyasi
    """
    result = df.copy()
    result[f"rsi_{period}"] = ta.rsi(result["close"], length=period)
    return result


def add_macd(
    df: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    """
    Moving Average Convergence Divergence (MACD) hesaplar ve DataFrame'e ekler.

    Parametreler
    ------------
    df     : pd.DataFrame  En az 'close' sutunu olan coin verisi
    fast   : int           Hizli EMA periyodu (varsayilan: 12)
    slow   : int           Yavas EMA periyodu (varsayilan: 26)
    signal : int           Sinyal hatti periyodu (varsayilan: 9)

    Eklenen sutunlar
    ----------------
    macd        : float  MACD cizgisi (hizli EMA - yavas EMA)
    macd_signal : float  Sinyal cizgisi (MACD'nin EMA'si)
    macd_hist   : float  Histogram (macd - macd_signal)

    Döndürür
    --------
    pd.DataFrame
    """
    result = df.copy()
    raw = ta.macd(result["close"], fast=fast, slow=slow, signal=signal)
    # pandas_ta cikti sutunlari: MACD_12_26_9, MACDh_12_26_9, MACDs_12_26_9
    result["macd"]        = raw[f"MACD_{fast}_{slow}_{signal}"]
    result["macd_hist"]   = raw[f"MACDh_{fast}_{slow}_{signal}"]
    result["macd_signal"] = raw[f"MACDs_{fast}_{slow}_{signal}"]
    return result


def add_bollinger_bands(
    df: pd.DataFrame,
    period: int = 20,
    std: float = 2.0,
) -> pd.DataFrame:
    """
    Bollinger Bands hesaplar ve DataFrame'e ekler.

    Parametreler
    ------------
    df     : pd.DataFrame  En az 'close' sutunu olan coin verisi
    period : int           Hareketli ortalama penceresi (varsayilan: 20)
    std    : float         Standart sapma katsayisi (varsayilan: 2.0)

    Eklenen sutunlar
    ----------------
    bb_upper : float  Ust bant
    bb_mid   : float  Orta bant (SMA)
    bb_lower : float  Alt bant

    Döndürür
    --------
    pd.DataFrame
    """
    result = df.copy()
    raw = ta.bbands(result["close"], length=period, std=std)
    # pandas_ta cikti sutunlari: BBL_20_2.0_2.0, BBM_20_2.0_2.0, BBU_20_2.0_2.0
    suffix = f"{period}_{std}_{std}"
    result["bb_lower"] = raw[f"BBL_{suffix}"]
    result["bb_mid"]   = raw[f"BBM_{suffix}"]
    result["bb_upper"] = raw[f"BBU_{suffix}"]
    return result


def add_ema(
    df: pd.DataFrame,
    periods: list = None,
) -> pd.DataFrame:
    """
    Birden fazla periyot icin Exponential Moving Average (EMA) hesaplar.

    Parametreler
    ------------
    df      : pd.DataFrame  En az 'close' sutunu olan coin verisi
    periods : list[int]     EMA periyotlari (varsayilan: [7, 14, 21, 50])

    Eklenen sutunlar
    ----------------
    ema_7, ema_14, ema_21, ema_50 : float  Ilgili periyot EMA degerleri

    Döndürür
    --------
    pd.DataFrame
    """
    if periods is None:
        periods = [7, 14, 21, 50]

    result = df.copy()
    for p in periods:
        result[f"ema_{p}"] = ta.ema(result["close"], length=p)
    return result


def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Average True Range (ATR) hesaplar ve DataFrame'e ekler.

    Parametreler
    ------------
    df     : pd.DataFrame  'high', 'low', 'close' sutunlarini iceren coin verisi
    period : int           ATR pencere uzunlugu (varsayilan: 14)

    Eklenen sutun
    -------------
    atr_14 : float  Volatilite olcumu (fiyat birimiyle)

    Döndürür
    --------
    pd.DataFrame
    """
    result = df.copy()
    result[f"atr_{period}"] = ta.atr(
        result["high"], result["low"], result["close"], length=period
    )
    return result


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tum teknik indikatörleri sirayla hesaplar ve DataFrame'e ekler.

    Uygulama sirasi: RSI -> MACD -> Bollinger Bands -> EMA -> ATR

    NOT: NaN temizligi burada yapilmaz. engineering.py icindeki
    prepare_features() sonunda tek seferinde dropna() uygulanir.

    Parametreler
    ------------
    df : pd.DataFrame
        date-index'li, ticker sutunu olmayan tek coin verisi.
        Gereken sutunlar: open, high, low, close

    Eklenen sutunlar
    ----------------
    rsi_14, macd, macd_signal, macd_hist,
    bb_upper, bb_mid, bb_lower,
    ema_7, ema_14, ema_21, ema_50,
    atr_14

    Döndürür
    --------
    pd.DataFrame  Indikatör sutunlari eklenmis kopya
    """
    result = df.copy()
    result = add_rsi(result)
    result = add_macd(result)
    result = add_bollinger_bands(result)
    result = add_ema(result)
    result = add_atr(result)
    return result
