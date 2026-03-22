# CLAUDE.md – Kripto Tahmin Platformu

## Proje Hakkında

Bu proje, Kaggle'dan alınan günlük kripto para fiyat verilerini kullanarak iki farklı tahmin görevi gerçekleştirir:

1. **Yön Sınıflandırması:** Ertesi günün kapanış fiyatı bugünden yüksek mi (1) yoksa düşük mü (0)?
2. **Getiri Tahmini:** Ertesi günün yüzde günlük getirisini regresyon ile tahmin etme.

**Veri kaynağı:** Kaggle – `svaningelgem/crypto-currencies-daily-prices`
**Hedef coinler:** BTC, ETH, LTC, XRP (src/load_data.py içindeki COINS listesinden değiştirilebilir)
**Modeller:** XGBoost (birincil), RandomForest (karşılaştırma)
**Arayüz:** Streamlit dashboard (dashboard/app.py)

---

## Veri Yapısı

### Ham CSV Sütunları
| Sütun  | Tip      | Açıklama                    |
|--------|----------|-----------------------------|
| ticker | str      | Coin sembolü (BTC, ETH, ...) |
| date   | datetime | Günlük tarih                |
| open   | float    | Açılış fiyatı               |
| high   | float    | Gün içi en yüksek           |
| low    | float    | Gün içi en düşük            |
| close  | float    | Kapanış fiyatı              |

> **UYARI:** Veri setinde `volume` sütunu YOKTUR.
> Volume bazlı indikatörler (OBV, MFI, VWAP vb.) kesinlikle kullanılmaz.

### İşlenmiş Veri
- `data/processed/{ticker}.csv` – coin bazında ayrılmış OHLC verisi
- `data/processed/{ticker}_features.csv` – tüm indikatör ve feature'ların eklendiği nihai veri

### Veri Akışı

```
data/raw/crypto_prices.csv
        │
        ▼ load_data.py (split_and_save)
data/processed/BTC.csv, ETH.csv, LTC.csv, XRP.csv
        │
        ▼ indicators.py (add_all_indicators)
        ▼ engineering.py (prepare_features)
data/processed/BTC_features.csv, ...
        │
        ▼ models.py (train_classifier / train_regressor)
models_saved/BTC_clf_xgboost.pkl, BTC_reg_xgboost.pkl, ...
        │
        ▼ dashboard/app.py (Streamlit)
```

---

## Kritik Kurallar

1. **Zamansal bölme:** `temporal_train_test_split()` içinde `shuffle=False` – zaman serisi karıştırılmaz.
2. **Feature dışı sütunlar:** `EXCLUDE_COLS = ["direction", "daily_return", "ticker", "open", "high", "low", "close"]` – bu sütunlar modele feature olarak girmez.
3. **Volume yasağı:** Volume bazlı hiçbir indikatör eklenmez.
4. **Model + scaler birlikte kaydedilir:** Model kaydedilirken varsa ilgili scaler da aynı isim ön eki ile `models_saved/` içine kaydedilir. Örnek: `BTC_clf_xgboost_scaler.pkl`
5. **NaN temizliği:** `indicators.py`'de yapılmaz; `prepare_features()` sonunda tek seferde `dropna()` uygulanır.

---

## Modül Sorumlulukları

| Dosya               | Sorumlu Ekip Üyesi | Görev |
|---------------------|--------------------|-------|
| src/load_data.py    | Üye 1              | Ham CSV okuma, coin bazında bölme ve kaydetme |
| src/indicators.py   | Üye 2              | RSI, MACD, Bollinger Bands, EMA, ATR hesaplama |
| src/engineering.py  | Üye 3              | Lag, rolling, fiyat türevli feature'lar ve hedef değişkenler |
| src/models.py       | Üye 4              | Model eğitimi, zamansal bölme, model kaydetme/yükleme |
| src/evaluate.py     | Üye 5              | Sınıflandırma ve regresyon metrik fonksiyonları |
| dashboard/app.py    | Üye 6              | Streamlit arayüzü, grafik ve metrik kartları |

---

## Branch ve Commit Kuralları

### Branch İsimlendirme
```
feature/load-data-pipeline
feature/ohlc-indicators
fix/rsi-nan-sorunu
```

### Commit Mesajı Formatı
```
feat(load_data): ham CSV okuma ve coin bölme fonksiyonları
feat(indicators): RSI ve MACD hesaplama eklendi
fix(models): zamansal bölme shuffle hatası düzeltildi
```

### Git Akışı
- `main` branch'e doğrudan push yapılmaz.
- Her özellik için `feature/aciklama` branch'i açılır.
- Kod tamamlandıktan sonra Pull Request açılır.
- En az 1 ekip üyesi review yaptıktan sonra merge edilir.

---

## Yaygın Hatalar ve Çözümleri

### 1. pandas-ta Kurulum Sorunu
```bash
# Hata: pandas_ta module not found veya NumPy uyumsuzluğu
pip install pandas-ta==0.3.14b --no-deps
pip install numpy==1.26.4
```

### 2. CSV Dosya Yolu Hatası
```python
# Hata: FileNotFoundError: data/raw/crypto_prices.csv
# Çözüm: Notebook veya betiği proje kök dizininden çalıştır
# Veya Path(__file__).parent.parent ile mutlak yol kullan
```

### 3. XGBoost Feature Uyuşmazlığı
```
# Hata: Feature names must be the same as those used during fit
# Çözüm: Eğitimde kullanılan sütun listesini modelle birlikte kaydet
# get_feature_columns() çıktısını joblib ile ayrıca sakla
```

### 4. Streamlit ImportError
```bash
# Çalıştırma yöntemi – proje kökünden:
streamlit run dashboard/app.py
```
