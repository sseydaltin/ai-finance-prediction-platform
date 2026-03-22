# CLAUDE.md – Kripto Para Zaman Serisi ile Fiyat Yönü Sınıflandırması ve Günlük Getiri Tahmin Platformu

> Bu dosya, projeye dahil olan her ekip üyesi ve yapay zeka asistanı için birincil referans kaynağıdır.
> Kod yazmadan önce bu dosyayı baştan sona oku. Kurallara uymayan kod PR'da reddedilir.

---

## 1. Proje Hakkında

**Proje Adı:** Kripto Para Zaman Serisi ile Fiyat Yönü Sınıflandırması ve Günlük Getiri Tahmin Platformu

**Amaç:** 100 kripto paranın geçmiş günlük OHLC fiyat verilerini kullanarak iki farklı makine öğrenmesi görevi gerçekleştirmek:

1. **Yön Sınıflandırması (Classification):** Ertesi günün kapanış fiyatı bugünkünden yüksek mi (1) yoksa düşük mü (0)?
2. **Günlük Getiri Tahmini (Regression):** Ertesi günün yüzde günlük getirisini tahmin etmek.

**Ekip:** 5 kişi
**Süre:** 10 hafta
**Metodoloji:** Scrum (2 haftalık sprintler)
**IDE:** PyCharm
**AI Asistan:** Claude Code
**VCS:** GitHub

---

## 2. Veri Kaynağı ve Yapısı

### Kaynak

- **Platform:** Kaggle
- **Dataset:** `svaningelgem/crypto-currencies-daily-prices`
- **İndirme:** Kaggle'dan manuel olarak indirilir, `data/raw/` altına 100 adet ayrı CSV olarak gelir.
- **Birleştirme:** `python src/merge_raw.py` komutu ile tüm CSV'ler tek dosyada birleştirilir.
- **Çıktı:** `data/raw/crypto_prices.csv` – 100 coin, 229.359 satır

### Birleşik CSV Sütunları

| Sütun  | Tip      | Açıklama                        |
|--------|----------|---------------------------------|
| ticker | str      | Coin sembolü (BTC, ETH, ADA...) |
| date   | datetime | Günlük tarih (YYYY-MM-DD)       |
| open   | float    | Günlük açılış fiyatı            |
| high   | float    | Gün içi en yüksek fiyat         |
| low    | float    | Gün içi en düşük fiyat          |
| close  | float    | Günlük kapanış fiyatı           |

### UYARILAR – Mutlaka Oku

> **VOLUME SÜTUNU YOKTUR.**
> Veri setinde `volume` sütunu bulunmamaktadır. OBV, MFI, VWAP, CMF gibi
> hacim bazlı hiçbir indikatör hesaplanamaz ve kullanılmaz. pandas-ta'nın
> volume gerektiren fonksiyonları çağrılmaz. Bu kural ihlal edilirse
> hesaplamalar sessizce NaN üretir ve model kalitesi bozulur.

> **SABİT COINS LİSTESİ YOKTUR.**
> Eski CLAUDE.md'de `COINS = ["BTC", "ETH", "LTC", "XRP"]` gibi bir liste
> vardı. Bu liste artık kullanılmıyor. Tüm ticker'lar `get_all_tickers(df)`
> ile dinamik olarak okunur. Hiçbir yerde sabit coin listesi tanımlanmaz.

### Veri Akışı (Pipeline)

```
Kaggle → data/raw/BTC.csv, ETH.csv, ... (100 dosya)
                │
                ▼  python src/merge_raw.py  (tek seferlik)
        data/raw/crypto_prices.csv
                │
                ▼  load_filtered()  (src/load_data.py)
        Ham DataFrame – tüm coinler, temizlenmiş, tarihe göre sıralı
                │
                ▼  filter_coin(df, ticker)  (src/load_data.py)
        Tek coin DataFrame – date index'li
                │
                ▼  prepare_features(df)  (src/engineering.py)
                   ├── add_all_indicators()  (src/indicators.py)
                   ├── add_lag_features()
                   ├── add_rolling_features()
                   ├── add_price_features()
                   ├── add_target_variables()
                   └── dropna()  ← tek ve tek NaN temizleme noktası
        Feature DataFrame – 34 sütun, model için hazır
                │
                ▼  prepare_all_coins(df_raw)  (src/engineering.py)
        Tüm coinler birleşik – 224.459 satır × 35 sütun (ticker dahil)
                │
                ▼  temporal_train_test_split()  (src/models.py)
        X_train, X_test, y_train, y_test
                │
                ▼  train_classifier() / train_regressor()  (src/models.py)
        models_saved/{ticker}_{clf|reg}_{model_type}.pkl
                │
                ▼  streamlit run dashboard/app.py
        Kullanıcı arayüzü
```

---

## 3. Proje Klasör Yapısı

```
kripto-tahmin-platformu/
│
├── data/
│   ├── raw/
│   │   └── crypto_prices.csv       ← merge_raw.py ile oluşturulur
│   │                                  GIT'E EKLENMEz (.gitignore'da)
│   └── processed/                  ← şimdilik boş; ileride kullanılabilir
│
├── src/
│   ├── __init__.py                 ← boş, paket tanımı için gerekli
│   ├── merge_raw.py                ← TEK SEFERLİK çalıştırılır
│   │                                  100 ayrı CSV'yi birleştirir
│   │                                  Kullanım: python src/merge_raw.py
│   ├── load_data.py                ← VERİ GİRİŞ KAPISI – TAMAMLANDI ✅
│   │                                  Tüm modüller veriyi buradan alır
│   ├── indicators.py               ← TEKNİK İNDİKATÖRLER – TAMAMLANDI ✅
│   │                                  Yalnızca OHLC bazlı hesaplamalar
│   ├── engineering.py              ← ÖZNİTELİK MÜHENDİSLİĞİ – TAMAMLANDI ✅
│   │                                  Lag, rolling, hedef değişkenler
│   ├── models.py                   ← MODEL EĞİTİMİ – YAZILACAK ⬜
│   │                                  XGBoost, RF, LightGBM, LSTM
│   └── evaluate.py                 ← METRİK HESAPLAMA – YAZILACAK ⬜
│                                      Sınıflandırma + regresyon metrikleri
│
├── dashboard/
│   └── app.py                      ← STREAMLİT ARAYÜZÜ – YAZILACAK ⬜
│
├── models_saved/                   ← Eğitilmiş modeller (.pkl, .h5)
│   └── scalers/                    ← joblib ile kaydedilen scaler nesneleri
│
├── notebooks/
│   ├── 01_EDA.ipynb                ← YAZILACAK ⬜
│   ├── 02_preprocessing.ipynb      ← YAZILACAK ⬜
│   ├── 03_models.ipynb             ← YAZILACAK ⬜
│   └── 04_evaluation.ipynb         ← YAZILACAK ⬜
│
├── tests/
│   ├── __init__.py
│   ├── test_load_data.py           ← 5 test – hepsi geçiyor ✅
│   └── test_indicators.py          ← 7 test – hepsi geçiyor ✅
│
├── reports/
│   ├── ara_raporlar/               ← Sprint sonunda ekip raporları
│   └── sonuc_raporu/               ← Final raporu
│
├── .github/
│   └── workflows/
│       └── ci.yml                  ← Sadece ruff çalışır (testler lokalde)
│
├── pyproject.toml                  ← ruff + pytest yapılandırması
├── requirements.txt                ← Tüm bağımlılıklar
├── CLAUDE.md                       ← Bu dosya
└── README.md                       ← Proje özeti (kullanıcıya yönelik)
```

---

## 4. Mevcut Modüller – Detaylı Referans

### 4.1 `src/load_data.py` – TAMAMLANDI ✅

**Sorumluluk:** Ham CSV'yi okumak, kalite kontrolü yapmak, coin bazında filtrelemek.
**Kural:** Projedeki her modül veri almak için bu dosyayı kullanır. `pd.read_csv()` ile
doğrudan CSV okuyan başka bir modül yazılmaz.

#### Fonksiyonlar

```python
load_raw(filename="data/raw/crypto_prices.csv") -> pd.DataFrame
```
- `data/raw/crypto_prices.csv` dosyasını okur
- `date` sütununu `pd.to_datetime()` ile datetime'a dönüştürür
- `date` sütununa göre artan sırada sıralar (zaman serisi için zorunlu)
- Döndürür: ticker, date, open, high, low, close sütunları olan ham DataFrame

```python
get_all_tickers(df) -> list[str]
```
- `df["ticker"].unique()` ile tüm benzersiz ticker'ları çeker
- Alfabetik sıralar ve liste olarak döndürür
- Örnek çıktı: `["ADA", "BNB", "BTC", "DOGE", "ETH", ...]` – 100 eleman

```python
filter_coin(df, ticker: str) -> pd.DataFrame
```
- Tek bir coinin verilerini filtreler: `df[df["ticker"] == ticker]`
- `date` sütununu index yapar: `.set_index("date")`
- `ticker` sütununu düşürür (zaten filtrelenmiş, gerekmiyor)
- Döndürür: date-indexed, OHLC sütunları olan DataFrame

```python
check_data_quality(df, min_rows=365) -> pd.DataFrame
```
- Her coin için satır sayısını kontrol eder
- `min_rows`'dan az verisi olan coinleri filtreler (veriyle çalışılamaz)
- Bilgi: 100 coinin hepsi bu kontrolü geçti, hiçbiri elenmedi
- Döndürür: yeterli verisi olan coinlerin birleşik DataFrame'i

```python
load_filtered(filename="data/raw/crypto_prices.csv", min_rows=365) -> pd.DataFrame
```
- **ANA GİRİŞ NOKTASI** – diğer tüm modüller bu fonksiyonu çağırır
- `load_raw()` + `check_data_quality()` birleşimi
- Döndürür: temizlenmiş, sıralanmış, kalite kontrollü birleşik DataFrame

#### Kullanım Örneği

```python
from src.load_data import load_filtered, filter_coin, get_all_tickers

# Tüm veriyi yükle (her zaman buradan başla)
df = load_filtered()

# Belirli bir coini al
btc = filter_coin(df, "BTC")   # date-indexed, OHLC sütunları

# Tüm ticker'ların listesi
tickers = get_all_tickers(df)  # ["ADA", "BNB", "BTC", ...] 100 eleman
```

---

### 4.2 `src/indicators.py` – TAMAMLANDI ✅

**Sorumluluk:** Teknik analiz indikatörlerini hesaplamak.
**Kural 1:** Tüm fonksiyonlar `df.copy()` ile başlar – orijinal DataFrame hiçbir zaman değiştirilmez.
**Kural 2:** Yalnızca OHLC bazlı indikatörler – volume gerektiren hiçbir fonksiyon kullanılmaz.
**Kural 3:** NaN temizleme yapılmaz – bu `prepare_features()` sonunda tek seferde yapılır.

#### Fonksiyonlar

```python
add_rsi(df, period=14) -> pd.DataFrame
```
- RSI (Relative Strength Index) hesaplar
- Eklenen sütun: `rsi_14`
- Değer aralığı: 0–100 (30 altı oversold, 70 üstü overbought)

```python
add_macd(df, fast=12, slow=26, signal=9) -> pd.DataFrame
```
- MACD ve sinyal çizgisi hesaplar
- Eklenen sütunlar: `macd`, `macd_signal`, `macd_hist`
- `macd_hist = macd - macd_signal`

```python
add_bollinger_bands(df, period=20, std=2.0) -> pd.DataFrame
```
- Bollinger Bantları hesaplar
- Eklenen sütunlar: `bb_upper`, `bb_mid`, `bb_lower`
- `bb_mid` = 20 günlük hareketli ortalama
- `bb_upper/lower` = bb_mid ± 2 * standart sapma

```python
add_ema(df, periods=None) -> pd.DataFrame
```
- Üstel Hareketli Ortalama (EMA) hesaplar
- Varsayılan periyotlar: `[7, 14, 21, 50]`
- Eklenen sütunlar: `ema_7`, `ema_14`, `ema_21`, `ema_50`

```python
add_atr(df, period=14) -> pd.DataFrame
```
- ATR (Average True Range) – volatilite ölçüsü
- Eklenen sütun: `atr_14`
- Hesaplama: True Range'in 14 günlük ortalaması

```python
add_all_indicators(df) -> pd.DataFrame
```
- Yukarıdaki tüm fonksiyonları sırayla çağırır
- Tek çağrı ile tüm indikatörleri ekler
- **NaN TEMIZLEMEZ** – bu kasıtlı bir karardır

#### Beklenen Çıktı (BTC örneği)

- Giriş: 5.665 satır × 4 sütun (OHLC)
- Çıkış: 5.665 satır × 16 sütun (4 OHLC + 12 indikatör)
- Yeni sütunlar: `rsi_14`, `macd`, `macd_signal`, `macd_hist`, `bb_upper`, `bb_mid`, `bb_lower`, `ema_7`, `ema_14`, `ema_21`, `ema_50`, `atr_14`

---

### 4.3 `src/engineering.py` – TAMAMLANDI ✅

**Sorumluluk:** Lag feature'ları, rolling istatistikler, fiyat türevli özellikler ve hedef değişkenleri oluşturmak.
**Kural 1:** Tüm fonksiyonlar `df.copy()` ile başlar – orijinal DataFrame değiştirilmez.
**Kural 2:** `prepare_features()` tek bir coin için çalışır. Döngü dışarıda yapılır.
**Kural 3:** `ticker` sütunu `prepare_features()` içinde eklenmez – döngüde eklenir.
**Kural 4:** `dropna()` yalnızca `prepare_features()` sonunda bir kez çağrılır.

#### Fonksiyonlar

```python
add_lag_features(df, lags=None) -> pd.DataFrame
```
- Varsayılan lag'lar: `[1, 2, 3, 5, 7]`
- Eklenen sütunlar: `close_lag_1`, `close_lag_2`, `close_lag_3`, `close_lag_5`, `close_lag_7`
- Anlam: `close_lag_1` = dünkü kapanış fiyatı, `close_lag_2` = 2 gün önceki, vb.

```python
add_rolling_features(df, windows=None) -> pd.DataFrame
```
- Varsayılan pencereler: `[5, 10]`
- Eklenen sütunlar: `rolling_mean_5`, `rolling_std_5`, `rolling_mean_10`, `rolling_std_10`
- `close` sütunu üzerinden hesaplanır

```python
add_price_features(df) -> pd.DataFrame
```
- Fiyat bazlı türev özellikler:
  - `daily_range` = high − low (günlük volatilite)
  - `body_size` = |close − open| (mum gövde büyüklüğü)
  - `upper_shadow` = high − max(open, close) (üst fitil)
  - `lower_shadow` = min(open, close) − low (alt fitil)

```python
add_target_variables(df) -> pd.DataFrame
```
- İki hedef değişken ekler:
  - `direction` (int): `1` eğer yarınki close > bugünkü close, `0` değilse
  - `daily_return` (float): `(close.shift(-1) - close) / close * 100`
- **NOT:** Son satır her zaman `NaN` olur (yarının verisi yok). `dropna()` bunu temizler.

```python
prepare_features(df) -> pd.DataFrame
```
- TEK BİR COİN için tam pipeline:
  1. `add_all_indicators(df)`
  2. `add_lag_features(df)`
  3. `add_rolling_features(df)`
  4. `add_price_features(df)`
  5. `add_target_variables(df)`
  6. `df.dropna()` ← tüm NaN'lar burada temizlenir
- BTC sonucu: **5.616 satır × 34 sütun**
- Giriş: date-indexed OHLC DataFrame (filter_coin() çıktısı)

```python
prepare_all_coins(df_raw) -> pd.DataFrame
```
- TÜM COİNLER için pipeline:
  - `get_all_tickers()` ile ticker listesini alır
  - Her ticker için `filter_coin()` → `prepare_features()` çalıştırır
  - `ticker` sütununu döngüde ekler (prepare_features() içinde değil!)
  - `pd.concat()` ile birleştirir
- Sonuç: **224.459 satır × 35 sütun** (ticker sütunu dahil)

#### Kullanım Örneği

```python
from src.load_data import load_filtered, filter_coin
from src.engineering import prepare_features, prepare_all_coins

df_raw = load_filtered()

# Tek coin için
btc_ready = prepare_features(filter_coin(df_raw, "BTC"))
print(btc_ready.shape)  # (5616, 34)

# Tüm coinler için (yavaş, ~1-2 dakika)
df_all = prepare_all_coins(df_raw)
print(df_all.shape)  # (224459, 35)
```

---

## 5. Henüz Yazılmamış Modüller

### 5.1 `src/models.py` – YAZILACAK ⬜

**Sorumluluk:** Model eğitimi, zamansal bölme, model kaydetme/yükleme.

#### EXCLUDE_COLS – Kritik Sabite

```python
EXCLUDE_COLS = [
    "direction",      # hedef değişken (sınıflandırma) – feature olamaz
    "daily_return",   # hedef değişken (regresyon) – feature olamaz
    "ticker",         # kategorik kimlik – modele girmez
    "open",           # ham fiyat – data leakage riski
    "high",           # ham fiyat – data leakage riski
    "low",            # ham fiyat – data leakage riski
    "close",          # ham fiyat – data leakage riski
    "date",           # index veya sütun olabilir – modele girmez
]
```

#### Yazılacak Fonksiyonlar

```python
get_feature_columns(df) -> list[str]
```
- `EXCLUDE_COLS` dışındaki tüm sütunları döndürür
- Eğitimde ve tahminlerde aynı liste kullanılmalı (XGBoost feature uyuşmazlığını önler)
- Bu listeyi modelle birlikte kaydetmek önerilir

```python
temporal_train_test_split(df, test_ratio=0.2) -> tuple
```
- **SHUFFLE=FALSE** – zaman serisi karıştırılmaz, bu kural değiştirilemez
- İlk %80 train, son %20 test (kronolojik sırada)
- Döndürür: `X_train, X_test, y_train, y_test`
- Neden önemli: Rastgele bölme gelecekteki veriyi eğitime karıştırır (data leakage)

```python
train_classifier(X_train, y_train, ticker, model_type="xgboost") -> model
```
- `model_type` seçenekleri: `"xgboost"`, `"random_forest"`, `"lightgbm"`, `"logistic"`
- Eğitilen modeli `models_saved/{ticker}_clf_{model_type}.pkl` olarak kaydeder
- Varsa scaler'ı `models_saved/scalers/{ticker}_clf_{model_type}_scaler.pkl` olarak kaydeder

```python
train_regressor(X_train, y_train, ticker, model_type="xgboost") -> model
```
- `model_type` seçenekleri: `"xgboost"`, `"random_forest"`, `"lightgbm"`, `"linear"`
- Eğitilen modeli `models_saved/{ticker}_reg_{model_type}.pkl` olarak kaydeder

```python
train_all_coins(df_raw, clf_models, reg_models) -> dict
```
- Tüm ticker'lar üzerinde döngü
- Her coin × her model kombinasyonu için eğitim
- Sonuçları sözlük olarak döndürür

```python
load_model(filepath) -> model
```
- `joblib.load(filepath)` ile modeli yükler
- Dosya yoksa açıklayıcı hata mesajı fırlatır

#### Model Kayıt Formatı

```
models_saved/
├── BTC_clf_xgboost.pkl
├── BTC_clf_xgboost_features.pkl    ← feature sütun listesi
├── BTC_clf_random_forest.pkl
├── BTC_reg_xgboost.pkl
├── BTC_reg_lightgbm.pkl
├── ETH_clf_xgboost.pkl
└── scalers/
    ├── BTC_clf_xgboost_scaler.pkl
    └── BTC_reg_xgboost_scaler.pkl
```

---

### 5.2 `src/evaluate.py` – YAZILACAK ⬜

**Sorumluluk:** Model performans metriklerini hesaplamak.

#### Yazılacak Fonksiyonlar

```python
classification_metrics(y_true, y_pred, y_prob=None) -> dict
```
- Döndürür: `accuracy`, `precision`, `recall`, `f1`, `roc_auc`
- `y_prob` verilmezse `roc_auc` hesaplanmaz

```python
regression_metrics(y_true, y_pred) -> dict
```
- Döndürür: `mae`, `mse`, `rmse`, `r2`, `mape`

```python
compare_models(results: dict) -> pd.DataFrame
```
- Birden fazla model sonucunu karşılaştırma tablosuna dönüştürür
- Giriş: `{model_name: metrics_dict}` formatında sözlük
- Çıkış: satır=model, sütun=metrik olan DataFrame

---

### 5.3 `dashboard/app.py` – YAZILACAK ⬜

**Sorumluluk:** Streamlit tabanlı kullanıcı arayüzü.
**Çalıştırma:** Proje kök dizininden `streamlit run dashboard/app.py`

#### Gereksinimler

- **Sidebar:**
  - Coin seçimi – `get_all_tickers()` ile dinamik liste (sabit liste değil)
  - Görev seçimi: Sınıflandırma / Regresyon
  - Model seçimi: XGBoost / Random Forest / LightGBM / LSTM
- **Önbellekleme:**
  - `@st.cache_data` – CSV yükleme için
  - `@st.cache_resource` – model yükleme için (ağır nesneler)
- **Hata Durumu:** Model dosyası yoksa `st.warning()` ile kullanıcıyı bilgilendir, uygulama çökmesin
- **Grafikler:** Plotly veya Altair tercih edilir (matplotlib değil)

---

### 5.4 `notebooks/` – YAZILACAK ⬜

Sırayla yazılmalı:

| Notebook              | İçerik                                           |
|-----------------------|--------------------------------------------------|
| `01_EDA.ipynb`        | Veri keşfi, dağılımlar, eksik değer analizi      |
| `02_preprocessing.ipynb` | Pipeline çıktılarının doğrulanması, görselleştirme |
| `03_models.ipynb`     | Model eğitimi, hiperparametre denemeleri         |
| `04_evaluation.ipynb` | Karşılaştırmalı metrik analizi, grafikler        |

---

## 6. Kritik Kurallar

Bu kuralların her biri bir nedene dayanır. Neden önemli olduğunu anlamadan değiştirme.

### Kural 1: SHUFFLE=FALSE – Zamansal Bütünlük

```python
# YANLIŞ ❌
train_test_split(X, y, test_size=0.2, shuffle=True)

# DOĞRU ✅
temporal_train_test_split(df, test_ratio=0.2)  # shuffle=False
```

**Neden:** Zaman serisi verisinde geleceğin verisini shuffle ile eğitime karıştırmak
"data leakage" yaratır. Model gerçekte hiç görmediği veride yüksek skor alır,
ama gerçek dünyada başarısız olur. Zaman sırasını her zaman koru.

---

### Kural 2: EXCLUDE_COLS – Hedef Sızıntısını Önle

```python
# YANLIŞ ❌ – direction ve daily_return feature olarak kullanılmaz
X = df[["rsi_14", "macd", "direction", "daily_return"]]

# DOĞRU ✅
feature_cols = get_feature_columns(df)  # EXCLUDE_COLS dışındakileri döndürür
X = df[feature_cols]
```

**Neden:** `direction` ve `daily_return` tahmin etmek istediğimiz değişkenler.
Bunları feature olarak vermek modelin cevabı görmesi demektir – bu sızıntı (leakage).
Aynı şekilde ham fiyatlar (open, high, low, close) eğitime girmez çünkü feature
mühendisliği zaten bu değerleri dönüştürerek kullanmaktadır.

---

### Kural 3: VOLUME YOK – Veri Setinde Bulunmuyor

```python
# YANLIŞ ❌ – volume sütunu mevcut değil
df.ta.obv()   # OBV hesaplamak için volume lazım
df.ta.mfi()   # MFI için volume lazım

# DOĞRU ✅ – yalnızca OHLC bazlı indikatörler
add_rsi(df)
add_macd(df)
add_bollinger_bands(df)
add_ema(df)
add_atr(df)
```

**Neden:** Veri setinde `volume` sütunu hiç yoktur. pandas-ta'nın volume bazlı
fonksiyonları çağrıldığında sessizce NaN üretir veya hata fırlatır. Bu hatalar
tüm pipeline'ı bozar.

---

### Kural 4: df.copy() – Yan Etkisiz Fonksiyonlar

```python
# YANLIŞ ❌
def add_rsi(df):
    df["rsi_14"] = ...  # orijinali değiştirir
    return df

# DOĞRU ✅
def add_rsi(df):
    df = df.copy()       # kopya üzerinde çalış
    df["rsi_14"] = ...
    return df
```

**Neden:** Python'da DataFrame referansla geçer. `df.copy()` kullanılmazsa
orijinal veri değişir ve ardından çağrılan fonksiyonlar bozuk veriyle çalışır.
Bu hata fark edilmesi çok zor, sessiz bir bozulmaya neden olur.

---

### Kural 5: load_filtered() Kullan, load_raw() Değil

```python
# YANLIŞ ❌ – kalite kontrolü atlanıyor
df = pd.read_csv("data/raw/crypto_prices.csv")

# YANLIŞ ❌ – yine kalite kontrolü yok
df = load_raw()

# DOĞRU ✅ – kalite kontrolü dahil
df = load_filtered()
```

**Neden:** `load_filtered()`, `load_raw()` + `check_data_quality()` birleşimidir.
Yetersiz veri olan coinler elenir, tarih dönüşümü yapılır, sıralama garantilenir.

---

### Kural 6: prepare_features() Tek Coin İçin

```python
# YANLIŞ ❌ – fonksiyon içinde döngü yapma
def prepare_features(df):
    results = []
    for ticker in df["ticker"].unique():   # içerde döngü
        ...

# DOĞRU ✅ – fonksiyon tek coin alır, döngü dışarıda
for ticker in tickers:
    coin_df = filter_coin(df_raw, ticker)
    features = prepare_features(coin_df)
    features["ticker"] = ticker            # ticker dışarıda eklenir
    results.append(features)
```

**Neden:** Tek sorumluluk ilkesi. Her fonksiyon tek bir şey yapar.
`prepare_all_coins()` zaten bu döngüyü yönetir.

---

### Kural 7: ticker Sütununu prepare_features() Sonrası Ekle

```python
# YANLIŞ ❌
def prepare_features(df):
    df["ticker"] = "BTC"   # fonksiyon içinde ekleme
    ...

# DOĞRU ✅ – döngüde ekle
features = prepare_features(filter_coin(df_raw, ticker))
features["ticker"] = ticker
```

**Neden:** `prepare_features()` genel bir fonksiyondur. Ticker bilgisi
sadece birleştirme sırasında gereklidir.

---

### Kural 8: NaN Temizleme Tek Noktada

```python
# YANLIŞ ❌ – indicators.py içinde NaN temizleme
def add_rsi(df):
    df["rsi_14"] = ...
    df.dropna(inplace=True)   # YAPMA

# DOĞRU ✅ – sadece prepare_features() sonunda
def prepare_features(df):
    df = add_all_indicators(df)
    df = add_lag_features(df)
    ...
    df = df.dropna()          # TEK VE TEK BURADA
    return df
```

**Neden:** Her indikatör farklı sayıda NaN üretir (RSI 14, MACD 26 gün bekler).
Ara temizleme yapılırsa satır sayısı beklenmedik şekilde azalır ve hata ayıklamak zorlaşır.

---

## 7. Modeller

### Sınıflandırma (direction: 0 veya 1)

| Model              | Tür      | Açıklama                      |
|--------------------|----------|-------------------------------|
| Logistic Regression | Baseline | Basit, yorumlanabilir         |
| Random Forest      | Ana      | Ensemble, güçlü baseline      |
| XGBoost            | Ana      | Gradyan boosting, genellikle en iyi |
| LightGBM           | Ana      | Hızlı, büyük veri için uygun  |
| LSTM               | Derin    | Sekans bazlı, 60 gün lookback |

### Regresyon (daily_return: float)

| Model              | Tür      | Açıklama                      |
|--------------------|----------|-------------------------------|
| Linear Regression  | Baseline | Basit, yorumlanabilir         |
| Random Forest      | Ana      | Ensemble                      |
| XGBoost            | Ana      | Gradyan boosting              |
| LightGBM           | Ana      | Hızlı                         |
| LSTM               | Derin    | 60 gün lookback penceresi     |

### LSTM Detayları

- Framework: Keras (TensorFlow backend)
- Lookback penceresi: 60 gün
- Model kayıt formatı: `models_saved/{ticker}_clf_lstm.h5`
- Scaler zorunlu: MinMaxScaler – `models_saved/scalers/{ticker}_clf_lstm_scaler.pkl`
- Her coin için ayrı model eğitilir

---

## 8. Test ve CI/CD

### Testleri Lokalde Çalıştır

```bash
# Tüm testler
pytest tests/ -v

# Belirli bir test dosyası
pytest tests/test_load_data.py -v
pytest tests/test_indicators.py -v

# Hızlı kontrol (sadece başarısız testler göster)
pytest tests/ -q
```

**Mevcut test durumu:**
- `tests/test_load_data.py` – 5 test, hepsi geçiyor ✅
- `tests/test_indicators.py` – 7 test, hepsi geçiyor ✅

### Linting

```bash
# Stil kontrolü
ruff check src/

# Otomatik düzeltme
ruff check src/ --fix
```

### GitHub Actions (ci.yml)

CI/CD pipeline'da **yalnızca ruff çalışır**. Testler CI'da çalıştırılmıyor.

**Neden testler CI'da çalışmıyor:**
`pandas-ta` kütüphanesi PyPI'da Python 3.11 ile tam uyumlu değildir.
GitHub Actions ortamında kurulum sorunlu olduğundan testler CI'a taşınmamıştır.
Testleri her zaman **push etmeden önce lokalde çalıştır**.

---

## 9. Branch ve Commit Kuralları

### Branch İsimlendirme

```
feature/load-data-pipeline
feature/ohlc-indicators
feature/engineering-pipeline
feature/model-training
feature/streamlit-dashboard
fix/rsi-nan-sorunu
fix/temporal-split-shuffle
```

### Commit Mesajı Formatı

```
feat(load_data): ham CSV okuma ve kalite kontrol fonksiyonları
feat(indicators): RSI, MACD, Bollinger Bands, EMA, ATR eklendi
feat(engineering): lag ve rolling feature'lar, hedef değişkenler
fix(models): zamansal bölmede shuffle=False düzeltildi
fix(indicators): volume bazlı indikatör kaldırıldı
test(load_data): filter_coin ve get_all_tickers testleri
docs(claude): CLAUDE.md güncellendi
```

### Git Akışı

1. `main` branch'e doğrudan push yapılmaz (branch protection aktif)
2. Her özellik için yeni branch aç: `git checkout -b feature/aciklama`
3. Kodu tamamla, testleri lokalde çalıştır
4. Pull Request aç
5. En az 1 ekip üyesi code review yapar
6. Onay sonrası merge edilir

---

## 10. Kurulum (Projeye Yeni Başlayan İçin)

```bash
# 1. Repoyu klonla
git clone https://github.com/sseydaltin/kripto-tahmin-platformu.git
cd kripto-tahmin-platformu

# 2. Sanal ortam oluştur
python -m venv .venv

# 3. Sanal ortamı aktif et
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Bağımlılıkları yükle
pip install -r requirements.txt

# 5. Kaggle'dan veriyi indir
# Kaggle'a giriş yap → svaningelgem/crypto-currencies-daily-prices
# "Download" butonuna tıkla → ZIP dosyasını aç
# İçindeki 100 adet CSV dosyasını data/raw/ klasörüne koy

# 6. CSV'leri birleştir (tek seferlik)
python src/merge_raw.py
# Çıktı: data/raw/crypto_prices.csv (229.359 satır)

# 7. Veri yüklemesini test et
python src/load_data.py
# Başarılı çıktı: "100 ticker yüklendi, 229359 satır"

# 8. Testleri çalıştır
pytest tests/ -v
# Beklenen: 12 test, hepsi geçmeli

# 9. Streamlit dashboard (hazır olduğunda)
streamlit run dashboard/app.py
```

---

## 11. Sık Karşılaşılan Hatalar ve Çözümleri

### Hata 1: `data/raw/crypto_prices.csv` bulunamıyor

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/crypto_prices.csv'
```

**Neden:** `merge_raw.py` henüz çalıştırılmamış.

**Çözüm:**
```bash
# Önce Kaggle'dan 100 CSV'yi data/raw/ içine koy
python src/merge_raw.py
```

---

### Hata 2: `No module named 'src'`

```
ModuleNotFoundError: No module named 'src'
```

**Neden:** Python çalışma dizini proje kökü değil.

**Çözüm:**
```toml
# pyproject.toml içinde bu satır olmalı:
[tool.pytest.ini_options]
pythonpath = ["."]
```
Veya PyCharm'da: File → Settings → Project → Python Interpreter → Working directory = proje kökü

---

### Hata 3: XGBoost Feature İsmi Uyuşmazlığı

```
ValueError: Feature names must be the same as those used during fit
```

**Neden:** Eğitim ve tahmin sırasında farklı sütun listeleri kullanılmış.

**Çözüm:**
```python
# Eğitimde feature listesini kaydet
import joblib
feature_cols = get_feature_columns(X_train)
joblib.dump(feature_cols, f"models_saved/{ticker}_clf_xgboost_features.pkl")

# Tahminlerde aynı listeyi yükle
feature_cols = joblib.load(f"models_saved/{ticker}_clf_xgboost_features.pkl")
X_pred = df[feature_cols]
```

---

### Hata 4: `pandas-ta` Kurulum Sorunu

```
ImportError: No module named 'pandas_ta'
# veya
numpy.core._multiarray_umath hatası
```

**Çözüm:**
```bash
pip install pandas-ta==0.3.14b --no-deps
pip install numpy==1.26.4
```

---

### Hata 5: `direction` Sütununda Tüm NaN

```python
df["direction"].isna().all()  # True
```

**Neden:** `filter_coin()` çıktısını `prepare_features()` yerine doğrudan kullandın.

**Çözüm:**
```python
# YANLIŞ ❌
btc = filter_coin(df, "BTC")
btc["direction"]  # add_target_variables() çağrılmadı

# DOĞRU ✅
btc = prepare_features(filter_coin(df, "BTC"))
btc["direction"]  # artık 0 ve 1 içerir
```

---

### Hata 6: Son Satır NaN (direction)

**Durum:** `add_target_variables()` sonrası son satırda `direction = NaN`.

**Neden:** Son günün "yarınki" verisi olmadığı için `shift(-1)` NaN üretir. Bu beklenen bir durumdur.

**Çözüm:** `prepare_features()` sonunda `dropna()` bu satırı zaten temizler.

---

### Hata 7: Streamlit Çalışmıyor

```bash
# YANLIŞ ❌ – dashboard klasöründen çalıştırma
cd dashboard
streamlit run app.py

# DOĞRU ✅ – proje kökünden çalıştır
streamlit run dashboard/app.py
```

**Neden:** `src` modülleri proje kök dizininden import edilir. Alt klasörden
çalıştırıldığında Python path ayarı bozulur.

---

### Hata 8: CI'da Test Başarısız

**Durum:** GitHub Actions'da testler hata veriyor.

**Neden:** `ci.yml` kasıtlı olarak yalnızca ruff çalıştırır. `pandas-ta` CI
ortamında kurulum sorunu yaşıyor.

**Çözüm:** Testleri lokalde çalıştır, CI'daki test hatalarını dikkate alma.

---

## 12. Modül Sorumlulukları

| Dosya                | Sorumlu | Durum          | Görev                                           |
|----------------------|---------|----------------|-------------------------------------------------|
| `src/merge_raw.py`   | Üye 1   | Tamamlandı ✅  | 100 CSV'yi birleştirip crypto_prices.csv oluşturma |
| `src/load_data.py`   | Üye 1   | Tamamlandı ✅  | Ham CSV okuma, kalite kontrol, coin filtreleme  |
| `src/indicators.py`  | Üye 2   | Tamamlandı ✅  | RSI, MACD, Bollinger, EMA, ATR hesaplama        |
| `src/engineering.py` | Üye 3   | Tamamlandı ✅  | Lag, rolling, fiyat feature'ları, hedef değişkenler |
| `src/models.py`      | Üye 4   | Yazılacak ⬜   | Model eğitimi, zamansal bölme, kayıt/yükleme   |
| `src/evaluate.py`    | Üye 5   | Yazılacak ⬜   | Sınıflandırma ve regresyon metrik fonksiyonları |
| `dashboard/app.py`   | Üye 5   | Yazılacak ⬜   | Streamlit arayüzü, grafik ve metrik kartları    |
