import pandas as pd
import pandas_ta as ta

# NOT: Veri setinde volume sütunu YOKTUR.
# Sadece OHLC bazlı indikatörler kullanılacak.


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = df.copy()
    df[f"rsi_{period}"] = ta.rsi(df["close"], length=period)
    return df


def add_macd(df: pd.DataFrame, fast: int = 12,
             slow: int = 26, signal: int = 9) -> pd.DataFrame:
    df = df.copy()
    raw = ta.macd(df["close"], fast=fast, slow=slow, signal=signal)
    df["macd"] = raw[f"MACD_{fast}_{slow}_{signal}"]
    df["macd_hist"] = raw[f"MACDh_{fast}_{slow}_{signal}"]
    df["macd_signal"] = raw[f"MACDs_{fast}_{slow}_{signal}"]
    return df


def add_bollinger_bands(df: pd.DataFrame, period: int = 20,
                        std: float = 2.0) -> pd.DataFrame:
    df = df.copy()
    raw = ta.bbands(df["close"], length=period, std=std)
    suffix = f"{period}_{std}_{std}"
    df["bb_lower"] = raw[f"BBL_{suffix}"]
    df["bb_mid"] = raw[f"BBM_{suffix}"]
    df["bb_upper"] = raw[f"BBU_{suffix}"]
    return df


def add_ema(df: pd.DataFrame,
            periods: list = None) -> pd.DataFrame:
    if periods is None:
        periods = [7, 14, 21, 50]
    df = df.copy()
    for p in periods:
        df[f"ema_{p}"] = ta.ema(df["close"], length=p)
    return df


def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = df.copy()
    df[f"atr_{period}"] = ta.atr(df["high"], df["low"], df["close"], length=period)
    return df


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = add_rsi(df)
    df = add_macd(df)
    df = add_bollinger_bands(df)
    df = add_ema(df)
    df = add_atr(df)
    return df
