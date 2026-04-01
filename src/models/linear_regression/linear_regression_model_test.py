import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.models.linear_regression.linear_regression_model import (
    create_features_and_target,
    evaluate_model,
    prepare_data,
    split_data,
)

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_DIR = BASE_DIR / "models_saved" / "linear_regression"


def load_model(coin):
    """
    Eğitilmiş modeli diskten yükler (.pkl formatında).
    CLAUDE.md formatı: {ticker}_reg_linear.pkl
    """
    model_path = MODEL_DIR / f"{coin}_reg_linear.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Model dosyası bulunamadı: {model_path}")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    return model


# ---------------------------------------------------------------------------
# Fixture – sentetik OHLC verisi
# MACD (26 gün) + lag_7 + rolling_10 = minimum ~50 satır gerekir.
# 150 satır kullanıyoruz; dropna() sonrası yeterli veri kalır.
# ---------------------------------------------------------------------------

@pytest.fixture
def ohlc_df():
    """150 günlük sentetik, date-indexed OHLC DataFrame'i döndürür."""
    np.random.seed(0)
    dates = pd.date_range("2022-01-01", periods=150, freq="D")
    close = 100 + np.cumsum(np.random.randn(150))
    df = pd.DataFrame(
        {
            "open": close * 0.99,
            "high": close * 1.02,
            "low": close * 0.98,
            "close": close,
        },
        index=dates,
    )
    df.index.name = "date"
    return df


@pytest.fixture
def prepared_df(ohlc_df):
    """prepare_data() pipeline'ından geçirilmiş DataFrame."""
    return prepare_data(ohlc_df)


# ---------------------------------------------------------------------------
# prepare_data() testleri
# ---------------------------------------------------------------------------

def test_prepare_data_adds_daily_return(prepared_df):
    """Pipeline sonrası daily_return sütunu olmalı."""
    assert "daily_return" in prepared_df.columns


def test_prepare_data_adds_direction(prepared_df):
    """Pipeline sonrası direction sütunu olmalı ve yalnızca 0/1 içermeli."""
    assert "direction" in prepared_df.columns
    assert set(prepared_df["direction"].unique()).issubset({0, 1})


def test_prepare_data_no_nan(prepared_df):
    """dropna() sonrası hiç NaN kalmamalı (Kural 8)."""
    assert not prepared_df.isnull().values.any()


def test_prepare_data_no_mutation(ohlc_df):
    """prepare_data() orijinal DataFrame'i değiştirmemeli (Kural 4)."""
    original_cols = list(ohlc_df.columns)
    prepare_data(ohlc_df)
    assert list(ohlc_df.columns) == original_cols


# ---------------------------------------------------------------------------
# split_data() testleri
# ---------------------------------------------------------------------------

def test_split_data_ratio(prepared_df):
    """Train %80, test %20 olmalı (Kural 1, CLAUDE.md)."""
    train, test = split_data(prepared_df)
    total = len(prepared_df)
    assert len(train) == int(total * 0.8)
    assert len(test) == total - int(total * 0.8)


def test_split_data_preserves_order(prepared_df):
    """Zamansal sıra korunmalı; train sonu test başından önce gelmeli (Kural 1)."""
    train, test = split_data(prepared_df)
    assert train.index[-1] < test.index[0]


# ---------------------------------------------------------------------------
# create_features_and_target() testleri
# ---------------------------------------------------------------------------

def test_create_features_excludes_ohlc(prepared_df):
    """X'te ham OHLC sütunları bulunmamalı (Kural 2 / EXCLUDE_COLS)."""
    X, _ = create_features_and_target(prepared_df, "daily_return")
    for col in ["open", "high", "low", "close"]:
        assert col not in X.columns, f"EXCLUDE_COLS ihlali: '{col}' feature'da"


def test_create_features_target_is_daily_return(prepared_df):
    """y hedef dizisi daily_return ile aynı olmalı."""
    _, y = create_features_and_target(prepared_df, "daily_return")
    pd.testing.assert_series_equal(y, prepared_df["daily_return"])


# ---------------------------------------------------------------------------
# evaluate_model() testleri
# ---------------------------------------------------------------------------

def test_evaluate_model_returns_five_metrics():
    """evaluate_model() mae, mse, rmse, r2, mape döndürmeli."""
    y_true = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    y_pred = np.array([1.1, 2.1, 2.9, 4.2, 4.8])
    result = evaluate_model(y_true, y_pred)
    assert len(result) == 5, "Beklenen 5 metrik: mae, mse, rmse, r2, mape"


def test_evaluate_model_rmse_equals_sqrt_mse():
    """RMSE = sqrt(MSE) olmalı."""
    y_true = pd.Series([1.0, 2.0, 3.0])
    y_pred = np.array([1.5, 2.5, 3.5])
    mae, mse, rmse, r2, mape = evaluate_model(y_true, y_pred)
    assert abs(rmse - mse ** 0.5) < 1e-9


# ---------------------------------------------------------------------------
# load_model() testi
# ---------------------------------------------------------------------------

def test_load_model_raises_if_missing():
    """Model dosyası yoksa FileNotFoundError fırlatılmalı."""
    with pytest.raises(FileNotFoundError):
        load_model("NONEXISTENT_COIN_XYZ")
