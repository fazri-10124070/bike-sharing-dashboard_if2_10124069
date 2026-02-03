import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.title("🚲 Bike Sharing Interactive Dashboard")
st.write("Analisis pola penyewaan sepeda berdasarkan cuaca, musim, jam, dan tren tahunan.")

# Load data
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# ================= SIDEBAR =================
st.sidebar.header("Filter Data")
year_option = st.sidebar.selectbox("Pilih Tahun", [2011, 2012])

df_day = df_day[df_day['yr'] == (year_option-2011)]
df_hour = df_hour[df_hour['yr'] == (year_option-2011)]

# ================= CUACA =================
st.header("🌦️ Pengaruh Cuaca terhadap Penyewaan")

weather_labels = {
    1: "Cerah",
    2: "Berkabut/Berawan",
    3: "Hujan Ringan/Salju",
    4: "Cuaca Parah"
}
df_day["weather_label"] = df_day["weathersit"].map(weather_labels)

weather_group = df_day.groupby("weather_label")["cnt"].mean()

st.line_chart(weather_group)
st.info("Cuaca cerah menghasilkan penyewaan sepeda paling tinggi.")

# ================= JAM =================
st.header("⏰ Pola Penyewaan Per Jam")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rata-rata Semua Hari")
    hourly = df_hour.groupby('hr')['cnt'].mean()
    st.line_chart(hourly)

with col2:
    st.subheader("Weekday vs Weekend")
    weekday = df_hour[df_hour['workingday']==1].groupby('hr')['cnt'].mean()
    weekend = df_hour[df_hour['workingday']==0].groupby('hr')['cnt'].mean()
    compare = pd.DataFrame({"Weekday": weekday, "Weekend": weekend})
    st.line_chart(compare)

st.info("Weekday memiliki puncak jam komuter, weekend puncak di siang hari.")

# ================= MUSIM =================
st.header("🍂 Penyewaan Berdasarkan Musim")

season_labels = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
df_day["season_label"] = df_day["season"].map(season_labels)

season_group = df_day.groupby("season_label")["cnt"].mean()
st.bar_chart(season_group)

st.info("Fall dan Summer menjadi musim dengan penyewaan tertinggi.")

# ================= TREN =================
st.header("📈 Tren Penyewaan Tahunan")

year_group = pd.read_csv('day.csv').groupby('yr')['cnt'].mean()
st.line_chart(year_group)

st.info("Terlihat peningkatan signifikan penggunaan sepeda dari 2011 ke 2012.")
