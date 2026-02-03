import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🚲 Bike Sharing Dashboard")

# Load data
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

# Ubah tanggal
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# Sidebar filter
st.sidebar.header("Filter Data")
year = st.sidebar.selectbox("Pilih Tahun", df_day['yr'].unique())

df_day = df_day[df_day['yr'] == year]
df_hour = df_hour[df_hour['yr'] == year]

# =========================
# 1. Pengaruh Cuaca
# =========================
st.header("Pengaruh Cuaca terhadap Penyewaan")

weather_labels = {
    1: "Cerah",
    2: "Berkabut/Berawan",
    3: "Hujan Ringan/Salju",
    4: "Cuaca Parah"
}

df_day["weather_label"] = df_day["weathersit"].map(weather_labels)
weather_group = df_day.groupby("weather_label")["cnt"].mean()

st.line_chart(weather_group)

# =========================
# 2. Pola Per Jam
# =========================
st.header("Pola Penyewaan Per Jam")

hourly = df_hour.groupby('hr')['cnt'].mean()
st.line_chart(hourly)

# =========================
# 3. Musim
# =========================
st.header("Penyewaan Berdasarkan Musim")

season_labels = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

df_day["season_label"] = df_day["season"].map(season_labels)
season_group = df_day.groupby("season_label")["cnt"].mean()

st.bar_chart(season_group)

# =========================
# 4. Tren Tahunan
# =========================
st.header("Tren Tahunan")

year_group = df_day.groupby("yr")["cnt"].mean()
st.line_chart(year_group)
