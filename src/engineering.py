import numpy as np
import pandas as pd

from src.indicators import add_all_indicators
from src.load_data import filter_coin, get_all_tickers


def add_lag_features(df: pd.DataFrame,
                     lags: list = None) -> pd.DataFrame:
    if lags is None:
        lags = [1, 2, 3, 5, 7]
    df = df.copy()
    for lag in lags:
        df[f"close_lag_{lag}"] = df["close"].shift(lag)
    return df


def add_rolling_features(df: pd.DataFrame,
                         windows: list = None) -> pd.DataFrame:
    if windows is None:
        windows = [5, 10]
    df = df.copy()
    for w in windows:
        df[f"rolling_mean_{w}"] = df["close"].rolling(w).mean()
        df[f"rolling_std_{w}"] = df["close"].rolling(w).std()
    return df


def add_price_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["daily_range"] = df["high"] - df["low"]
    df["body_size"] = (df["close"] - df["open"]).abs()
    df["upper_shadow"] = df["high"] - df[["open", "close"]].max(axis=1)
    df["lower_shadow"] = df[["open", "close"]].min(axis=1) - df["low"]
    return df


def add_target_variables(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["daily_return"] = df["close"].pct_change() * 100
    df["direction"] = (df["close"].shift(-1) > df["close"]).astype(float)
    # Son satırda direction NaN olur – prepare_features() sonunda dropna() temizler
    df.loc[df.index[-1], "direction"] = np.nan
    return df


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_all_indicators(df)
    df = add_lag_features(df)
    df = add_rolling_features(df)
    df = add_price_features(df)
    df = add_target_variables(df)
    df = df.dropna()
    df = df.reset_index()   # date index → sütun (EXCLUDE_COLS ile dışlanabilir)
    return df


def prepare_all_coins(df_raw: pd.DataFrame) -> pd.DataFrame:
    tickers = get_all_tickers(df_raw)
    results = []
    skipped = []
    for ticker in tickers:
        try:
            coin_df = filter_coin(df_raw, ticker)
            features = prepare_features(coin_df)
            features["ticker"] = ticker
            results.append(features)
        except Exception as exc:
            print(f"[prepare_all_coins] UYARI: {ticker} atlandı → {exc}")
            skipped.append(ticker)
    if not results:
        raise RuntimeError("Hiçbir coin başarıyla işlenmedi.")
    if skipped:
        print(f"[prepare_all_coins] Atlanan coinler ({len(skipped)}): {skipped}")
    return pd.concat(results, ignore_index=True)
