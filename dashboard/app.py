import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.load_data import COINS, load_processed
from src.evaluate import classification_metrics, regression_metrics

st.set_page_config(page_title="Kripto Tahmin Platformu", layout="wide")

# ── Sidebar ─────────────────────────────────────────────────────────────────
# ─
# TODO: st.sidebar.title ile başlık ekle
# TODO: st.sidebar.selectbox ile coin seçimi (COINS listesinden)
# TODO: st.sidebar.radio ile görev seçimi: "Sınıflandırma" / "Regresyon"

# ── Veri Yükleme ─────────────────────────────────────────────────────────────
# TODO: @st.cache_data decorator'lı fonksiyon yaz, load_processed() çağır
# TODO: veri yoksa st.warning() ile mesaj göster

# ── Model Yükleme ─────────────────────────────────────────────────────────────
# TODO: @st.cache_resource decorator'lı fonksiyon yaz, joblib.load() kullan
# TODO: model dosyası yoksa st.warning() göster ve st.stop() ile dur

# ── Ana Sayfa ─────────────────────────────────────────────────────────────────
# TODO: st.title ile sayfa başlığı

# ── Grafik ───────────────────────────────────────────────────────────────────
# TODO: son 90 günlük veriyi al
# TODO: model ile tahmin üret
# TODO: Plotly go.Figure() ile gerçek ve tahmin çizgilerini çiz
# TODO: st.plotly_chart ile göster

# ── Metrik Kartları ──────────────────────────────────────────────────────────
# TODO: st.columns(3) ile yan yana 3 kart oluştur
# TODO: Sınıflandırma seçiliyse: Accuracy, F1, yön tahmini (↑ / ↓)
# TODO: Regresyon seçiliyse: MAE, RMSE, R²
