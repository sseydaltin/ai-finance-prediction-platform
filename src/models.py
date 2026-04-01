from pathlib import Path

import pandas as pd

MODELS_DIR = Path("models_saved")

# Bu sütunlar asla model feature'ı olmaz
EXCLUDE_COLS = ["direction", "daily_return", "ticker",
                "open", "high", "low", "close"]


def get_feature_columns(df: pd.DataFrame) -> list:
    """
    EXCLUDE_COLS dışındaki tüm sütunları döndürür.
    Bunlar modele girecek feature sütunlarıdır.
    """
    return [col for col in df.columns if col not in EXCLUDE_COLS]


def temporal_train_test_split(df: pd.DataFrame, test_ratio: float = 0.2):
    """
    Zamansal bölme yapar – SHUFFLE YASAK.
    - İlk %80 train, son %20 test olacak şekilde böl
    - Bölme tarihini ekrana yazdır
    - get_feature_columns() ile X sütunlarını belirle
    Returns: X_train, X_test, y_clf_train, y_clf_test,
             y_reg_train, y_reg_test
    """
    # TODO: split_idx = int(len(df) * (1 - test_ratio))
    # TODO: train = df.iloc[:split_idx], test = df.iloc[split_idx:]
    # TODO: bölme tarihini yazdır
    # TODO: X = get_feature_columns() ile belirle
    # TODO: y_clf = direction, y_reg = daily_return sütunları
    # TODO: 6 değişkeni return et
    pass


def train_classifier(X_train, y_train, ticker: str,
                     model_type: str = "xgboost") -> object:
    """
    Sınıflandırma modeli eğitir ve kaydeder.
    - model_type 'xgboost' ise XGBClassifier kullan
    - model_type 'random_forest' ise RandomForestClassifier kullan
    - Kayıt yolu: models_saved/{ticker}_clf_{model_type}.pkl
    - Eğitim sonrası train accuracy'i yazdır
    """
    # TODO: model_type'a göre model nesnesi oluştur
    # TODO: model.fit(X_train, y_train)
    # TODO: train accuracy hesapla ve yazdır
    # TODO: joblib.dump() ile kaydet
    # TODO: eğitilmiş modeli döndür
    pass


def train_regressor(X_train, y_train, ticker: str,
                    model_type: str = "xgboost") -> object:
    """
    Regresyon modeli eğitir ve kaydeder.
    - model_type 'xgboost' ise XGBRegressor kullan
    - model_type 'random_forest' ise RandomForestRegressor kullan
    - Kayıt yolu: models_saved/{ticker}_reg_{model_type}.pkl
    - Eğitim sonrası train RMSE'yi yazdır
    """
    # TODO: model_type'a göre model nesnesi oluştur
    # TODO: model.fit(X_train, y_train)
    # TODO: train RMSE hesapla ve yazdır
    # TODO: joblib.dump() ile kaydet
    # TODO: eğitilmiş modeli döndür
    pass


def load_model(filename: str) -> object:
    """
    models_saved/ klasöründen .pkl modelini yükler.
    Dosya yoksa anlaşılır hata mesajı verir.
    """
    # TODO: dosya yolunu oluştur
    # TODO: dosya yoksa FileNotFoundError fırlat
    # TODO: joblib.load() ile yükle ve döndür
    pass
