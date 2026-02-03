import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ---------- THEME & STYLE ----------
st.markdown("""
<style>
body { background-color: #f4f6f8; }
h1, h2, h3 { color: #1f2937; }
.block-container { padding-top:2rem; }
.summary-text { font-size: 28px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🚲 Bike Sharing Dashboard")
st.caption("Dashboard interaktif, ringkas, siap Streamlit Cloud")

# ---------- LOAD DATA ----------
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# ---------- FILTER TAHUN ----------
year_option = st.selectbox("📅 Pilih Tahun", [2011, 2012])
df_day_filtered = df_day[df_day['yr'] == (year_option-2011)]
df_hour_filtered = df_hour[df_hour['yr'] == (year_option-2011)]

# ---------- RINGKASAN PENYEWAAN BESAR ----------
st.subheader("📌 Ringkasan Penyewaan")
m1, m2, m3 = st.columns(3)
if len(df_day_filtered) > 0:
    m1.markdown(f"<div class='summary-text'>📦 Total Penyewaan: {int(df_day_filtered['cnt'].sum()):,}</div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='summary-text'>📈 Rata-rata Harian: {int(df_day_filtered['cnt'].mean()):,}</div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='summary-text'>🏆 Hari Teramai: {df_day_filtered.loc[df_day_filtered['cnt'].idxmax(), 'dteday'].strftime('%d-%m-%Y')}</div>", unsafe_allow_html=True)
else:
    m1.markdown("<div class='summary-text'>📦 Total Penyewaan: 0</div>", unsafe_allow_html=True)
    m2.markdown("<div class='summary-text'>📈 Rata-rata Harian: 0</div>", unsafe_allow_html=True)
    m3.markdown("<div class='summary-text'>🏆 Hari Teramai: -</div>", unsafe_allow_html=True)

st.divider()

# ---------- TABS ----------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🌦️ Cuaca","⏰ Pola Jam","🔥 Heatmap","🍂 Musim","🔎 Clustering","📈 Tren Tahunan","🔮 Prediksi"
])

# ---------- TAB 1: CUACA ----------
with tab1:
    st.header("🌦️ Penyewaan Berdasarkan Cuaca")
    weather_labels = {1:"☀️ Cerah",2:"🌫️ Berkabut",3:"🌧️ Hujan Ringan",4:"⛈️ Cuaca Parah"}
    df_day_filtered["weather_label"] = df_day_filtered["weathersit"].map(weather_labels)
    weather_group = df_day_filtered.groupby("weather_label")["cnt"].mean().reset_index()
    fig_weather = px.line(weather_group, x="weather_label", y="cnt", markers=True,
                          labels={"cnt":"Rata-rata Penyewaan","weather_label":"Cuaca"})
    fig_weather.update_layout(title="Rata-rata Penyewaan per Cuaca", template="plotly_white")
    st.plotly_chart(fig_weather, use_container_width=True)

# ---------- TAB 2: POLA JAM ----------
with tab2:
    st.header("⏰ Pola Penyewaan per Jam")
    hourly = df_hour_filtered.groupby('hr')['cnt'].mean().reset_index()
    fig_hour = px.line(hourly, x='hr', y='cnt', markers=True, labels={"cnt":"Rata-rata Penyewaan","hr":"Jam"})
    fig_hour.update_layout(title="Rata-rata Penyewaan per Jam", template="plotly_white")
    st.plotly_chart(fig_hour, use_container_width=True)

# ---------- TAB 3: HEATMAP ----------
with tab3:
    st.header("🔥 Heatmap Jam vs Hari")
    df_hour_filtered['weekday'] = df_hour_filtered['dteday'].dt.day_name()
    heatmap_data = df_hour_filtered.groupby(['weekday','hr'])['cnt'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='weekday', columns='hr', values='cnt')
    order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    heatmap_pivot = heatmap_pivot.reindex(order)
    fig_heat = px.imshow(heatmap_pivot, labels=dict(x="Jam",y="Hari",color="Rata-rata Penyewaan"))
    fig_heat.update_layout(title="Heatmap Jam vs Hari", template="plotly_white")
    st.plotly_chart(fig_heat, use_container_width=True)

# ---------- TAB 4: MUSIM ----------
with tab4:
    st.header("🍂 Rata-rata Penyewaan per Musim")
    season_labels = {1:"🌸 Spring",2:"☀️ Summer",3:"🍂 Fall",4:"❄️ Winter"}
    df_day_filtered["season_label"] = df_day_filtered["season"].map(season_labels)
    season_group = df_day_filtered.groupby("season_label")["cnt"].mean().reset_index()
    fig_season = px.bar(season_group, x="season_label", y="cnt", text="cnt", labels={"cnt":"Rata-rata Penyewaan","season_label":"Musim"})
    fig_season.update_layout(title="Rata-rata Penyewaan per Musim", template="plotly_white")
    st.plotly_chart(fig_season, use_container_width=True)

# ---------- TAB 5: CLUSTERING ----------
with tab5:
    st.header("🔎 Scatter Clustering Sepi–Normal–Ramai")
    q1 = df_day_filtered['cnt'].quantile(0.33)
    q2 = df_day_filtered['cnt'].quantile(0.66)
    def cluster_label(cnt):
        if cnt <= q1:
            return "🔵 Sepi"
        elif cnt <= q2:
            return "🟢 Normal"
        else:
            return "🔴 Ramai"
    df_day_filtered['cluster'] = df_day_filtered['cnt'].apply(cluster_label)
    fig_cluster = px.scatter(df_day_filtered, x='dteday', y='cnt', color='cluster', symbol='season_label',
                             size='cnt', hover_data=['season_label','weather_label'])
    fig_cluster.update_layout(title="Cluster Penyewaan", template="plotly_white")
    st.plotly_chart(fig_cluster, use_container_width=True)

# ---------- TAB 6: TREN TAHUNAN ----------
with tab6:
    st.header("📈 Tren Penyewaan Tahunan")
    year_group = df_day.groupby('yr')['cnt'].mean()
    year_group.index = [2011, 2012]
    fig_trend = px.line(x=year_group.index, y=year_group.values, markers=True, labels={"x":"Tahun","y":"Rata-rata Penyewaan"})
    fig_trend.update_layout(title="Tren Penyewaan Tahunan", template="plotly_white")
    st.plotly_chart(fig_trend, use_container_width=True)

# ---------- TAB 7: PREDIKSI ----------
with tab7:
    st.header("🔮 Prediksi Penyewaan Harian (Linear Regression)")
    df_pred = df_day_filtered.sort_values('dteday').reset_index()
    df_pred['day_number'] = np.arange(len(df_pred))
    X = df_pred[['day_number']]
    y = df_pred['cnt']
    model = LinearRegression()
    model.fit(X, y)
    future_days = 30
    future_X = np.arange(len(df_pred), len(df_pred)+future_days).reshape(-1,1)
    y_pred = model.predict(future_X)
    pred_dates = pd.date_range(df_pred['dteday'].max() + pd.Timedelta(days=1), periods=future_days)
    df_future = pd.DataFrame({'dteday':pred_dates, 'predicted_cnt':y_pred})
    df_plot = pd.concat([df_pred[['dteday','cnt']], df_future.rename(columns={'predicted_cnt':'cnt'})], ignore_index=True)
    df_plot['type'] = ['Actual']*len(df_pred) + ['Predicted']*future_days
    fig_pred = px.line(df_plot, x='dteday', y='cnt', color='type', markers=True)
    fig_pred.update_layout(title="Prediksi 30 Hari Kedepan", template="plotly_white")
    st.plotly_chart(fig_pred, use_container_width=True)
