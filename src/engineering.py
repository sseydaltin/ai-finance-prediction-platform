"""
Ozellik muhendisligi modulu.

Kural: Fonksiyonlar date-index'li, ticker sutunu olmayan tek coin
DataFrame'i alir. NaN temizligi yalnizca prepare_features() sonunda
tek seferinde dropna() ile yapilir.
"""

import pandas as pd

from src.indicators import add_all_indicators
from src.load_data import filter_coin, get_all_tickers


def add_lag_features(df: pd.DataFrame, lags: list = None) -> pd.DataFrame:
    """
    Kapanıs fiyati icin gecikme (lag) ozellikler ekler.

    Parametreler
    ------------
    df   : pd.DataFrame  En az 'close' sutunu olan coin verisi
    lags : list[int]     Gecikme adim listesi (varsayilan: [1, 2, 3, 5, 7])

    Eklenen sutunlar
    ----------------
    close_lag_1, close_lag_2, close_lag_3, close_lag_5, close_lag_7

    Döndürür
    --------
    pd.DataFrame
    """
    if lags is None:
        lags = [1, 2, 3, 5, 7]

    result = df.copy()
    for lag in lags:
        result[f"close_lag_{lag}"] = result["close"].shift(lag)
    return result


def add_rolling_features(df: pd.DataFrame, windows: list = None) -> pd.DataFrame:
    """
    Kayan pencere ortalamasi ve standart sapmasi ekler.

    Parametreler
    ------------
    df      : pd.DataFrame  En az 'close' sutunu olan coin verisi
    windows : list[int]     Pencere boyutlari (varsayilan: [5, 10, 20])

    Eklenen sutunlar
    ----------------
    rolling_mean_5, rolling_std_5,
    rolling_mean_10, rolling_std_10,
    rolling_mean_20, rolling_std_20

    Döndürür
    --------
    pd.DataFrame
    """
    if windows is None:
        windows = [5, 10, 20]

    result = df.copy()
    for w in windows:
        result[f"rolling_mean_{w}"] = result["close"].rolling(w).mean()
        result[f"rolling_std_{w}"]  = result["close"].rolling(w).std()
    return result


def add_price_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    OHLC'den turetilen mum (candlestick) ozellikler ekler.

    Eklenen sutunlar
    ----------------
    daily_range  : float  Gunluk fiyat araligi (high - low)
    body_size    : float  Mum govdesi buyuklugu abs(close - open)
    upper_shadow : float  Ust fitil uzunlugu (high - max(open, close))
    lower_shadow : float  Alt fitil uzunlugu (min(open, close) - low)

    Döndürür
    --------
    pd.DataFrame
    """
    result = df.copy()
    result["daily_range"]  = result["high"] - result["low"]
    result["body_size"]    = (result["close"] - result["open"]).abs()
    result["upper_shadow"] = result["high"] - result[["open", "close"]].max(axis=1)
    result["lower_shadow"] = result[["open", "close"]].min(axis=1) - result["low"]
    return result


def add_target_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Model icin iki hedef degisken ekler.

    Eklenen sutunlar
    ----------------
    direction    : int (0/1)  Ertesi gun kapanisi bugununkinden yuksekse 1
    daily_return : float (%)  Gunluk yuzde getiri: pct_change() * 100

    UYARI: Bu sutunlar modele feature olarak verilmez.
    EXCLUDE_COLS listesine dahil edilmelidir.

    NOT: direction'in son satiri her zaman NaN olur (ertesi gun bilinmez).
    Bu NaN prepare_features() sonundaki dropna() ile temizlenir.

    Döndürür
    --------
    pd.DataFrame
    """
    result = df.copy()
    result["daily_return"] = result["close"].pct_change() * 100
    result["direction"]    = (result["close"].shift(-1) > result["close"]).astype(float)
    # Son satir direction=NaN; dropna sonraya birakildi
    return result


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tum ozellik muhendisligi adimlarini pipeline olarak calistirir.

    Adim sirasi
    -----------
    1. add_all_indicators()   – RSI, MACD, BB, EMA, ATR
    2. add_lag_features()     – close gecikme ozellikleri
    3. add_rolling_features() – kayan pencere ortalama/std
    4. add_price_features()   – gunluk aralik, mum govdesi, fitil
    5. add_target_variables() – direction, daily_return
    6. dropna()               – tum NaN satirlari tek seferde temizle

    NOT: NaN temizligi yalnizca burada, en sonda yapilir.

    Parametreler
    ------------
    df : pd.DataFrame
        date-index'li, ticker sutunu olmayan tek coin verisi.
        Gereken sutunlar: open, high, low, close

    Döndürür
    --------
    pd.DataFrame  Modele hazir, NaN'siz ozellik matrisi
    """
    result = add_all_indicators(df)
    result = add_lag_features(result)
    result = add_rolling_features(result)
    result = add_price_features(result)
    result = add_target_variables(result)
    result = result.dropna()
    result.reset_index(inplace=True)   # date index -> sutun

    print(f"[prepare_features] shape: {result.shape}  |  sutun sayisi: {result.shape[1]}")
    return result


def prepare_all_coins(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Tum ticker'lar icin prepare_features() calistirir ve sonuclari birlestir.

    - get_all_tickers() ile tam coin listesini alir
    - Her coin icin filter_coin() + prepare_features() uygular
    - Hazir DataFrame'e 'ticker' sutunu ekler
    - Hatalı coinleri try/except ile atlar, uyari verir
    - Tum sonuclari pd.concat ile birlestirir

    Parametreler
    ------------
    df_raw : pd.DataFrame
        load_filtered() ciktisi; ticker ve OHLC sutunlarini icerir

    Döndürür
    --------
    pd.DataFrame
        Tum coinlerin birlestirilmis, modele hazir DataFrame'i.
        Sutunlar: date, open, high, low, close, [tum ozellikler], ticker
    """
    tickers = get_all_tickers(df_raw)
    frames = []
    skipped = []

    for ticker in tickers:
        try:
            coin_df  = filter_coin(df_raw, ticker)
            prepared = prepare_features(coin_df)
            prepared["ticker"] = ticker
            frames.append(prepared)
        except Exception as exc:
            print(f"[prepare_all_coins] UYARI: {ticker} atlandi -> {exc}")
            skipped.append(ticker)

    if not frames:
        raise RuntimeError("Hicbir coin basariyla islenmedi.")

    combined = pd.concat(frames, ignore_index=True)

    print(f"\n[prepare_all_coins] Tamamlandi")
    print(f"  Basarili coin : {len(frames)}")
    print(f"  Atlanan coin  : {len(skipped)}{' -> ' + str(skipped) if skipped else ''}")
    print(f"  Toplam satir  : {len(combined):,}")
    print(f"  Sutun sayisi  : {combined.shape[1]}")
    return combined
