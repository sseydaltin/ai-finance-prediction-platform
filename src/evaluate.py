import pandas as pd
import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, roc_auc_score, mean_absolute_error,
                              mean_squared_error, r2_score)


def classification_metrics(y_true, y_pred, y_prob=None) -> dict:
    """
    Sınıflandırma metriklerini hesaplar ve dict döndürür.
    Döndürülecek anahtarlar:
    - accuracy, precision, recall, f1
    - roc_auc (sadece y_prob verilmişse, yoksa None)
    """
    # TODO: accuracy_score, precision_score, recall_score, f1_score hesapla
    # TODO: y_prob verilmişse roc_auc_score hesapla, yoksa None
    # TODO: dict olarak döndür
    pass


def regression_metrics(y_true, y_pred) -> dict:
    """
    Regresyon metriklerini hesaplar ve dict döndürür.
    Döndürülecek anahtarlar:
    - mae, mse, rmse, r2, mape
    """
    # TODO: mean_absolute_error → mae
    # TODO: mean_squared_error → mse
    # TODO: mse'nin karekökü → rmse
    # TODO: r2_score → r2
    # TODO: mean absolute percentage error → mape
    # TODO: dict olarak döndür
    pass


def compare_models(results: dict) -> pd.DataFrame:
    """
    Birden fazla modelin metriklerini karşılaştıran tablo oluşturur.
    Girdi: {"XGBoost": metrics_dict, "RandomForest": metrics_dict}
    Çıktı: model isimleri satır, metrikler sütun olan DataFrame
    DataFrame'i hem döndür hem de konsola güzel formatlı yazdır.
    """
    # TODO: pd.DataFrame(results).T ile tablo oluştur
    # TODO: print ile konsola yazdır
    # TODO: DataFrame'i döndür
    pass
