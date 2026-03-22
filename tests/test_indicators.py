import pytest

from src.indicators import (
    add_all_indicators,
    add_atr,
    add_bollinger_bands,
    add_ema,
    add_macd,
    add_rsi,
)
from src.load_data import filter_coin, load_filtered


@pytest.fixture(scope="module")
def btc_df():
    """BTC verisini bir kez yükle, modül kapsamında tüm testlerde kullan."""
    df = load_filtered()
    return filter_coin(df, "BTC")


def test_add_rsi_creates_column(btc_df):
    result = add_rsi(btc_df)
    assert "rsi_14" in result.columns


def test_add_macd_creates_columns(btc_df):
    result = add_macd(btc_df)
    assert "macd" in result.columns
    assert "macd_signal" in result.columns
    assert "macd_hist" in result.columns


def test_add_bollinger_creates_columns(btc_df):
    result = add_bollinger_bands(btc_df)
    assert "bb_upper" in result.columns
    assert "bb_mid" in result.columns
    assert "bb_lower" in result.columns


def test_add_ema_creates_columns(btc_df):
    result = add_ema(btc_df)
    for p in [7, 14, 21, 50]:
        assert f"ema_{p}" in result.columns


def test_add_atr_creates_column(btc_df):
    result = add_atr(btc_df)
    assert "atr_14" in result.columns


def test_add_all_indicators_no_data_loss(btc_df):
    result = add_all_indicators(btc_df)
    # NaN temizleme yapılmıyor; satır sayısı değişmemeli
    assert len(result) == len(btc_df)


def test_original_df_not_modified(btc_df):
    original_cols = set(btc_df.columns)
    add_rsi(btc_df)
    # add_rsi df.copy() kullandığı için orijinal df değişmemeli
    assert set(btc_df.columns) == original_cols
