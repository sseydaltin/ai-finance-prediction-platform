# Kripto Para Fiyat Yönü Sınıflandırması ve Getiri Tahmin Platformu

Günlük OHLC verisi kullanarak kripto para fiyat yönünü sınıflandıran ve günlük getiriyi tahmin eden makine öğrenmesi platformu.

---

## Kurulum

### 1. Repoyu klonla
```bash
git clone <repo-url>
cd kripto-tahmin-platformu
```

### 2. Sanal ortam oluştur ve aktif et
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Bağımlılıkları yükle
```bash
pip install -r requirements.txt
```

### 4. Veriyi indir ve yerleştir
Kaggle'dan aşağıdaki veri setini indir:
> https://www.kaggle.com/datasets/svaningelgem/crypto-currencies-daily-prices

İndirilen CSV dosyasını şu konuma kaydet:
```
data/raw/crypto_prices.csv
```

### 5. Veriyi coin bazında böl
```bash
python src/load_data.py
```
Bu komut `data/processed/` klasörüne BTC.csv, ETH.csv, LTC.csv, XRP.csv dosyalarını oluşturur.

---

## Çalıştırma Sırası

```
01_EDA.ipynb          → Keşifsel veri analizi
02_preprocessing.ipynb → İndikatörler ve feature mühendisliği
03_models.ipynb        → Model eğitimi ve kaydetme
04_evaluation.ipynb    → Test seti değerlendirmesi
```

Son adım olarak Streamlit dashboard'u başlat:
```bash
streamlit run dashboard/app.py
```

---

## Coin Listesini Değiştirmek

`src/load_data.py` dosyasındaki `COINS` listesini düzenle:

```python
# Varsayılan
COINS = ["BTC", "ETH", "LTC", "XRP"]

# Örnek değişiklik
COINS = ["BTC", "ETH", "ADA", "SOL", "DOT"]
```

Değişiklikten sonra `python src/load_data.py` komutunu tekrar çalıştır.

> **Not:** Veri setinde bulunmayan ticker'lar uyarı verir ama hata vermez.

---

## Proje Yapısı

```
kripto-tahmin-platformu/
├── data/
│   ├── raw/                → Kaggle CSV burada
│   └── processed/          → Coin bazında ayrılmış CSV'ler
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_models.ipynb
│   └── 04_evaluation.ipynb
├── src/
│   ├── load_data.py        → Veri yükleme ve bölme
│   ├── indicators.py       → Teknik indikatörler (OHLC bazlı)
│   ├── engineering.py      → Feature mühendisliği
│   ├── models.py           → Model eğitimi ve kaydetme
│   └── evaluate.py         → Metrik hesaplama
├── dashboard/
│   └── app.py              → Streamlit arayüzü
├── models_saved/           → Eğitilmiş modeller (.pkl)
├── reports/
│   ├── ara_raporlar/
│   └── sonuc_raporu/
├── requirements.txt
├── CLAUDE.md               → Geliştirici kılavuzu
└── README.md
```

---

## Katkı Sağlama

```bash
# Yeni branch aç
git checkout -b feature/gorev-adi

# Kodunu yaz ve test et

# Commit at
git add src/ilgili_dosya.py
git commit -m "feat(modul): yapılan değişikliğin kısa açıklaması"

# Pull Request aç
git push origin feature/gorev-adi
# GitHub/GitLab üzerinden PR oluştur → ekip review → merge
```

**Commit format:** `feat|fix|docs|refactor(modül): açıklama`
**main branch'e doğrudan push yapılmaz.**
