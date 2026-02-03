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
</style>
""", unsafe_allow_html=True)

st.title("🚲 Bike Sharing Dashboard")
st.caption("Dashboard interaktif, data mining, prediksi, CSV download, siap Streamlit Cloud")

# ---------- LOAD DATA ----------
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

# ---------- SIDEBAR FILTER ----------
st.sidebar.header("🔍 Filter Data")
year_option = st.sidebar.selectbox("📅 Pilih Tahun", [2011, 2012])
df_day_filtered = df_day[df_day['yr'] == (year_option-2011)]
df_hour_filtered = df_hour[df_hour['yr'] == (year_option-2011)]

# Season Filter
season_labels = {1:"🌸 Spring",2:"☀️ Summer",3:"🍂 Fall",4:"❄️ Winter"}
df_day_filtered["season_label"] = df_day_filtered["season"].map(season_labels)
season_options = st.sidebar.multiselect("🌿 Pilih Musim", options=season_labels.values(), default=list(season_labels.values()))
df_day_filtered = df_day_filtered[df_day_filtered["season_label"].isin(season_options)]
df_hour_filtered = df_hour_filtered[df_hour_filtered["season"].map(season_labels).isin(season_options)]

# Weather Filter
weather_labels = {1:"☀️ Cerah",2:"🌫️ Berkabut",3:"🌧️ Hujan Ringan",4:"⛈️ Cuaca Parah"}
df_day_filtered["weather_label"] = df_day_filtered["weathersit"].map(weather_labels)
weather_options = st.sidebar.multiselect("🌦️ Pilih Cuaca", options=weather_labels.values(), default=list(weather_labels.values()))
df_day_filtered = df_day_filtered[df_day_filtered["weather_label"].isin(weather_options)]
df_hour_filtered = df_hour_filtered[df_hour_filtered["weathersit"].map(weather_labels).isin(weather_options)]

# Clustering
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

cluster_options = st.sidebar.multiselect("📊 Pilih Cluster", options=["🔵 Sepi","🟢 Normal","🔴 Ramai"], default=["🔵 Sepi","🟢 Normal","🔴 Ramai"])
df_day_filtered = df_day_filtered[df_day_filtered['cluster'].isin(cluster_options)]
df_hour_filtered = df_hour_filtered[df_hour_filtered['dteday'].isin(df_day_filtered['dteday'])]

selected_cluster = st.sidebar.selectbox("⏰ Pilih Cluster untuk Pola Jam", options=["Semua"] + ["🔵 Sepi","🟢 Normal","🔴 Ramai"])
if selected_cluster != "Semua":
    df_hour_cluster = df_hour_filtered[df_hour_filtered['dteday'].isin(df_day_filtered[df_day_filtered['cluster']==selected_cluster]['dteday'])]
else:
    df_hour_cluster = df_hour_filtered.copy()

# ---------- METRICS TANPA KOTAK PUTIH ----------
st.subheader("📌 Ringkasan Penyewaan")
m1, m2, m3 = st.columns(3)
if len(df_day_filtered) > 0:
    m1.write(f"📦 **Total Penyewaan:** {int(df_day_filtered['cnt'].sum()):,}")
    m2.write(f"📈 **Rata-rata Harian:** {int(df_day_filtered['cnt'].mean()):,}")
    m3.write(f"🏆 **Hari Teramai:** {df_day_filtered.loc[df_day_filtered['cnt'].idxmax(), 'dteday'].strftime('%d-%m-%Y')}")
else:
    m1.write("📦 **Total Penyewaan:** 0")
    m2.write("📈 **Rata-rata Harian:** 0")
    m3.write("🏆 **Hari Teramai:** -")

st.divider()

# ---------- TABS ----------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🌦️ Cuaca","⏰ Pola Jam","🔥 Heatmap","🍂 Musim","🔎 Clustering","📈 Tren Tahunan","🔮 Prediksi"
])

# ---------- TAB 1: CUACA ----------
with tab1:
    st.header("🌦️ Penyewaan Berdasarkan Cuaca")
    if len(df_day_filtered) > 0:
        weather_group = df_day_filtered.groupby("weather_label")["cnt"].mean().reindex(weather_options).reset_index()
        fig_weather = px.line(weather_group, x="weather_label", y="cnt", markers=True,
                              labels={"cnt":"Rata-rata Penyewaan","weather_label":"Cuaca"})
        fig_weather.update_layout(title="Rata-rata Penyewaan per Cuaca", template="plotly_white")
        st.plotly_chart(fig_weather, use_container_width=True)
        st.download_button("📥 Download CSV", weather_group.to_csv(index=False).encode('utf-8'), "weather_data.csv","text/csv")

# ---------- TAB 2: POLA JAM ----------
with tab2:
    st.header(f"⏰ Pola Jam - Cluster: {selected_cluster}")
    if len(df_hour_cluster) > 0:
        hourly = df_hour_cluster.groupby('hr')['cnt'].mean().reset_index()
        fig_hour = px.line(hourly, x='hr', y='cnt', markers=True, labels={"cnt":"Rata-rata Penyewaan","hr":"Jam"})
        fig_hour.update_layout(title=f"Pola Jam - Cluster: {selected_cluster}", template="plotly_white")
        st.plotly_chart(fig_hour, use_container_width=True)
        st.download_button("📥 Download CSV", hourly.to_csv(index=False).encode('utf-8'), "hourly_data.csv","text/csv")

# ---------- TAB 3: HEATMAP ----------
with tab3:
    st.header("🔥 Heatmap Jam vs Hari")
    if len(df_hour_cluster) > 0:
        df_hour_cluster['weekday'] = df_hour_cluster['dteday'].dt.day_name()
        heatmap_data = df_hour_cluster.groupby(['weekday','hr'])['cnt'].mean().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='weekday', columns='hr', values='cnt')
        order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        heatmap_pivot = heatmap_pivot.reindex(order)
        fig_heat = px.imshow(heatmap_pivot, labels=dict(x="Jam",y="Hari",color="Rata-rata Penyewaan"))
        fig_heat.update_layout(title=f"Heatmap Jam vs Hari - Cluster: {selected_cluster}", template="plotly_white")
        st.plotly_chart(fig_heat, use_container_width=True)
        st.download_button("📥 Download CSV", heatmap_data.to_csv(index=False).encode('utf-8'), "heatmap_data.csv","text/csv")

# ---------- TAB 4: MUSIM ----------
with tab4:
    st.header("🍂 Rata-rata Penyewaan per Musim")
    if len(df_day_filtered) > 0:
        season_group = df_day_filtered.groupby("season_label")["cnt"].mean().reindex(season_options).reset_index()
        fig_season = px.bar(season_group, x="season_label", y="cnt", text="cnt", labels={"cnt":"Rata-rata Penyewaan","season_label":"Musim"})
        fig_season.update_layout(title="Rata-rata Penyewaan per Musim", template="plotly_white")
        st.plotly_chart(fig_season, use_container_width=True)
        st.download_button("📥 Download CSV", season_group.to_csv(index=False).encode('utf-8'), "season_data.csv","text/csv")

# ---------- TAB 5: CLUSTERING ----------
with tab5:
    st.header("🔎 Scatter Clustering Sepi–Normal–Ramai per Musim")
    if len(df_day_filtered) > 0:
        fig_cluster = px.scatter(df_day_filtered, x='dteday', y='cnt', color='cluster', symbol='season_label',
                                 size='cnt', hover_data=['season_label','weather_label'])
        fig_cluster.update_layout(title="Cluster per Musim", template="plotly_white")
        st.plotly_chart(fig_cluster, use_container_width=True)
        st.download_button("📥 Download CSV", df_day_filtered.to_csv(index=False).encode('utf-8'), "cluster_data.csv","text/csv")

# ---------- TAB 6: TREN TAHUNAN ----------
with tab6:
    st.header("📈 Tren Penyewaan Tahunan")
    year_group = pd.read_csv('day.csv').groupby('yr')['cnt'].mean()
    year_group.index = [2011, 2012]
    fig_trend = px.line(x=year_group.index, y=year_group.values, markers=True, labels={"x":"Tahun","y":"Rata-rata Penyewaan"})
    fig_trend.update_layout(title="Tren Penyewaan Tahunan", template="plotly_white")
    st.plotly_chart(fig_trend, use_container_width=True)
    st.download_button("📥 Download CSV", pd.DataFrame({'Tahun':[2011,2012],'Rata-rata Penyewaan':year_group.values}).to_csv(index=False).encode('utf-8'), "yearly_trend.csv","text/csv")

# ---------- TAB 7: PREDIKSI ----------
with tab7:
    st.header("🔮 Prediksi Penyewaan Harian (Linear Regression)")
    if len(df_day_filtered) > 0:
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
        st.download_button("📥 Download CSV Prediksi", df_plot.to_csv(index=False).encode('utf-8'), "prediction_data.csv","text/csv")
