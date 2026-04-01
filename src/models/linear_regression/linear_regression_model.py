import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    r2_score,
)

from src.engineering import prepare_features
from src.load_data import filter_coin, get_all_tickers, load_filtered
from src.models import get_feature_columns

# Tüm satırların terminalde görünmesini sağlar (debug / inceleme için)
pd.set_option('display.max_rows', None)

# Proje dizinlerini tanımla
BASE_DIR = Path(__file__).resolve().parents[3]


def load_coin_data(df_raw, coin):
    """
    load_filtered() çıktısından belirtilen coin'in verisini döndürür.
    Kural 5: Veri mutlaka load_filtered() → filter_coin() pipeline'ı üzerinden okunur.
    """
    return filter_coin(df_raw, coin)


def prepare_data(df):
    """
    Coin DataFrame'ini tam feature engineering pipeline'ından geçirir.
    Proje hedefleri:
      - Regresyon  : daily_return (yüzde günlük getiri)
      - Sınıflandırma: direction (0/1)
    prepare_features() indikatörleri, lag/rolling feature'ları ve hedef
    değişkenleri ekler; NaN'ları tek seferde temizler (Kural 8).
    """
    return prepare_features(df)


def split_data(df):
    """
    Zaman sırasını bozmadan %80 train - %20 test olarak ayırır.
    Kural 1: shuffle=False – zaman serisi karıştırılmaz.
    CLAUDE.md: temporal_train_test_split(test_ratio=0.2)
    """
    split_index = int(len(df) * 0.8)
    train = df.iloc[:split_index]
    test = df.iloc[split_index:]
    return train, test



def create_features_and_target(df, target_column):
    """
    Model giriş (X) ve hedef (y) değişkenlerini oluşturur.
    Kural 2: EXCLUDE_COLS dışındaki sütunlar feature olarak kullanılır.
    Ham OHLC (open, high, low, close) feature olamaz.
    """
    feature_cols = get_feature_columns(df)
    X = df[feature_cols]
    y = df[target_column]
    return X, y


def train_linear_regression(X_train, y_train):
    """
    Linear Regression modelini eğitir.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def make_predictions(model, X_test):
    """
    Eğitilmiş model ile test verisi üzerinde tahmin üretir.
    """
    predictions = model.predict(X_test)
    return predictions


def compare_predictions(y_test, predictions, target_name, n=5):
    """
    İlk n adet gerçek ve tahmin değerini karşılaştırmalı olarak gösterir.
    """
    result_df = pd.DataFrame({
        f"Gercek_{target_name}": y_test.values[:n],
        f"Tahmin_{target_name}": predictions[:n]
    })
    return result_df


def evaluate_model(y_true, predictions):
    """
    Model performansını ölçer:
    MAE, MSE, RMSE, R2, MAPE
    src/evaluate.py regression_metrics() spec'i ile uyumlu.
    """
    mae = mean_absolute_error(y_true, predictions)
    mse = mean_squared_error(y_true, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, predictions)
    mape = mean_absolute_percentage_error(y_true, predictions)
    return mae, mse, rmse, r2, mape


def evaluate_train_test(model, X_train, y_train, X_test, y_test):
    """
    Train ve test setleri üzerinde ayrı ayrı performans hesaplar.
    Overfitting analizi için kullanılır.
    """
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    train_mae, train_mse, train_rmse, train_r2, train_mape = evaluate_model(y_train, train_pred)
    test_mae, test_mse, test_rmse, test_r2, test_mape = evaluate_model(y_test, test_pred)

    return train_mae, train_mse, train_rmse, train_r2, train_mape, test_mae, test_mse, test_rmse, test_r2, test_mape


def save_model(model, coin, target_name):
    """
    Eğitilmiş modeli disk'e kaydeder (.pkl formatında)
    Her coin ve target için ayrı model oluşturulur.
    """
    model_dir = BASE_DIR / "models_saved" / "linear_regression"
    model_dir.mkdir(parents=True, exist_ok=True)

    model_path = model_dir / f"{coin}_{target_name}_linear.pkl"

    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Model kaydedildi: {model_path}")


if __name__ == "__main__":
    # Veriyi pipeline üzerinden yükle (tek seferlik)
    df_raw = load_filtered()

    # Tüm coinleri al
    coins = get_all_tickers(df_raw)
    print(f"Toplam coin sayısı: {len(coins)}")

    # Regresyon hedefi: daily_return (CLAUDE.md tanımı)
    TARGET_COLUMN = "daily_return"

    results = []

    # Her coin için model eğit
    for coin in coins:
        print(f"\n==================== {coin} ====================")

        df = load_coin_data(df_raw, coin)
        df = prepare_data(df)  # prepare_features() pipeline'ı çalıştırır

        train, test = split_data(df)

        print(f"Toplam veri: {len(df)}")
        print(f"Train: {len(train)}")
        print(f"Test: {len(test)}")

        X_train, y_train = create_features_and_target(train, TARGET_COLUMN)
        X_test, y_test = create_features_and_target(test, TARGET_COLUMN)

        # Model eğit ve tahmin yap
        model = train_linear_regression(X_train, y_train)
        predictions = make_predictions(model, X_test)

        # Performans ölç
        comparison = compare_predictions(y_test, predictions, TARGET_COLUMN, n=5)
        mae, mse, rmse, r2, mape = evaluate_model(y_test, predictions)

        # Train vs Test performansı (overfitting kontrolü)
        (train_mae, train_mse, train_rmse, train_r2, train_mape,
         test_mae, test_mse, test_rmse, test_r2, test_mape) = evaluate_train_test(
            model, X_train, y_train, X_test, y_test
        )

        # Modeli kaydet: CLAUDE.md formatı → {ticker}_reg_linear.pkl
        save_model(model, coin, "reg")

        # Sonuçları listeye ekle
        results.append({
            "coin": coin,
            "target": TARGET_COLUMN,
            "toplam_veri": len(df),
            "train_sayisi": len(train),
            "test_sayisi": len(test),
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "r2": r2,
            "mape": mape,
            "train_mae": train_mae,
            "train_mse": train_mse,
            "train_rmse": train_rmse,
            "train_r2": train_r2,
            "train_mape": train_mape,
            "test_mae": test_mae,
            "test_mse": test_mse,
            "test_rmse": test_rmse,
            "test_r2": test_r2,
            "test_mape": test_mape,
            "r2_gap": train_r2 - test_r2  # overfitting göstergesi
        })

        # Debug / analiz çıktıları
        print(f"X_train shape: {X_train.shape}")
        print(f"y_train shape: {y_train.shape}")
        print(f"X_test shape: {X_test.shape}")
        print(f"y_test shape: {y_test.shape}")
        print(f"Tahmin sayısı: {len(predictions)}")
        print(f"MAE : {mae}")
        print(f"MSE : {mse}")
        print(f"RMSE: {rmse}")
        print(f"R2  : {r2}")
        print(f"MAPE: {mape}")
        print(f"Train MAE : {train_mae}")
        print(f"Train RMSE: {train_rmse}")
        print(f"Train R2  : {train_r2}")
        print(f"Test  MAE : {test_mae}")
        print(f"Test  RMSE: {test_rmse}")
        print(f"Test  R2  : {test_r2}")
        print(f"R2 Gap    : {train_r2 - test_r2}")
        print(comparison)

    # Tüm sonuçları DataFrame'e çevir
    results_df = pd.DataFrame(results)

    # r2_gap'e göre sırala
    results_df = results_df.sort_values(by="r2_gap", ascending=False).reset_index(drop=True)

    print("\n=== TUM COIN SONUCLARI ===")
    print(results_df)

    # Sonuçları CSV olarak kaydet
    output_path = BASE_DIR / "reports" / "linear_regression_results.csv"
    results_df.to_csv(output_path, index=False)
    print(f"\nSonuçlar kaydedildi: {output_path}")
