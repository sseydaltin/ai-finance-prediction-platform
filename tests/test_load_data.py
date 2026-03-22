import pandas as pd

from src.load_data import filter_coin, get_all_tickers, load_filtered


def test_load_filtered_returns_dataframe():
    df = load_filtered()
    assert isinstance(df, pd.DataFrame)


def test_load_filtered_has_required_columns():
    df = load_filtered()
    required = ["ticker", "date", "open", "high", "low", "close"]
    for col in required:
        assert col in df.columns, f"Eksik sütun: {col}"


def test_get_all_tickers_returns_list():
    df = load_filtered()
    tickers = get_all_tickers(df)
    assert isinstance(tickers, list)
    assert len(tickers) > 0


def test_filter_coin_returns_single_ticker():
    df = load_filtered()
    btc_df = filter_coin(df, "BTC")
    # date index'li, sadece BTC satırları – index uzunluğu > 0 olmalı
    assert len(btc_df) > 0


def test_data_quality_min_rows():
    df = load_filtered(min_rows=365)
    counts = df.groupby("ticker").size()
    assert (counts >= 365).all(), "Bazı coinlerde 365'ten az satır var"
