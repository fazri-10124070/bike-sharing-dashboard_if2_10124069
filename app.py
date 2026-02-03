import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ---------- WHITE CLEAN STYLE ----------
st.markdown("""
    <style>
    body { background-color: #ffffff; }
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #1f2937; }
    .stMetric {
        background-color: #f9fafb;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚲 Bike Sharing Interactive Dashboard")
st.caption("Analisis pola penyewaan sepeda berdasarkan cuaca, musim, waktu, dan tren tahunan")

# ---------- LOAD DATA ----------
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# ---------- SIDEBAR ----------
st.sidebar.header("🔍 Filter Data")
year_option = st.sidebar.selectbox("Pilih Tahun", [2011, 2012])

df_day = df_day[df_day['yr'] == (year_option-2011)]
df_hour = df_hour[df_hour['yr'] == (year_option-2011)]

# ---------- METRICS ----------
st.subheader("📌 Ringkasan Penyewaan")

m1, m2, m3 = st.columns(3)
m1.metric("Total Penyewaan", f"{int(df_day['cnt'].sum()):,}")
m2.metric("Rata-rata Harian", f"{int(df_day['cnt'].mean()):,}")
m3.metric("Hari Teramai", df_day.loc[df_day['cnt'].idxmax(), 'dteday'].date())

st.divider()

# ---------- CUACA ----------
st.header("🌦️ Pengaruh Cuaca terhadap Penyewaan")

weather_labels = {1:"Cerah",2:"Berkabut",3:"Hujan Ringan",4:"Cuaca Parah"}
df_day["weather_label"] = df_day["weathersit"].map(weather_labels)
weather_group = df_day.groupby("weather_label")["cnt"].mean()

st.line_chart(weather_group)
st.caption("Cuaca cerah menghasilkan rata-rata penyewaan sepeda paling tinggi.")

# ---------- JAM ----------
st.header("⏰ Pola Penyewaan Per Jam")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Rata-rata Semua Hari")
    hourly = df_hour.groupby('hr')['cnt'].mean()
    st.line_chart(hourly)

with c2:
    st.subheader("Weekday vs Weekend")
    weekday = df_hour[df_hour['workingday']==1].groupby('hr')['cnt'].mean()
    weekend = df_hour[df_hour['workingday']==0].groupby('hr')['cnt'].mean()
    st.line_chart(pd.DataFrame({"Weekday": weekday, "Weekend": weekend}))

st.divider()

# ---------- MUSIM ----------
st.header("🍂 Penyewaan Berdasarkan Musim")

season_labels = {1:"Spring",2:"Summer",3:"Fall",4:"Winter"}
df_day["season_label"] = df_day["season"].map(season_labels)
season_group = df_day.groupby("season_label")["cnt"].mean()

st.bar_chart(season_group)
st.caption("Musim Fall dan Summer menjadi periode dengan penyewaan tertinggi.")

st.divider()

# ---------- TREN ----------
st.header("📈 Tren Penyewaan Tahunan")

year_group = pd.read_csv('day.csv').groupby('yr')['cnt'].mean()
st.line_chart(year_group)
st.caption("Terlihat peningkatan signifikan penggunaan sepeda dari tahun 2011 ke 2012.")
