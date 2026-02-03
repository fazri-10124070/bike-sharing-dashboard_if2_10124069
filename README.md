# Bike Sharing Data Analysis 
![Dashboard Preview](dashboard.png)

Proyek ini merupakan analisis data Bike Sharing untuk memahami pola penyewaan sepeda berdasarkan faktor cuaca, musim, waktu, dan tren tahunan.  
Hasil analisis disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

---

## Anggota Kelompok IF2

| NIM | Nama |
|-----|------|
| 10123318 | Jorge Fielnero Sauman |
| 10124051 | Raden Rama Feryl Alfaro |
| 10124064 | M. Rifqi Afriza Fasha |
| 10124069 | Deni Solehudin |
| 10124070 | Fazri Hariri |

---

## Pertanyaan Bisnis

1. Bagaimana pengaruh cuaca terhadap jumlah penyewaan sepeda?
2. Pada jam berapa penyewaan sepeda paling tinggi, dan apakah berbeda antara hari kerja vs weekend?
3. Musim apa yang memiliki jumlah penyewaan sepeda tertinggi?
4. Faktor lingkungan apa yang paling mempengaruhi jumlah penyewaan (suhu, kelembapan, angin)?
5. Apakah terdapat tren peningkatan penggunaan sepeda dari 2011 ke 2012?

---

## Tahapan Analisis Data

Analisis dilakukan melalui beberapa tahapan:

- Data Wrangling (Gathering, Assessing, Cleaning)
- Exploratory Data Analysis (EDA)
- Visualization & Explanatory Analysis
- Penerapan teknik Data Mining (Clustering K-Means) untuk menemukan pola hari sepi, normal, dan ramai
- Pembuatan Dashboard Interaktif menggunakan Streamlit

Notebook analisis lengkap tersedia pada file ".ipynb" di repository ini.

---

## Hasil Insight Utama

- Cuaca cerah menghasilkan jumlah penyewaan tertinggi
- Weekday memiliki dua puncak (08.00 & 17.00), weekend puncak di siang hari
- Musim Fall dan Summer memiliki penyewaan tertinggi
- Suhu merupakan faktor lingkungan paling berpengaruh
- Terjadi peningkatan signifikan penggunaan sepeda dari tahun 2011 ke 2012
- Clustering menunjukkan kombinasi suhu, kelembapan, angin, dan kondisi hari membentuk pola permintaan sepeda

---

## Dashboard Interaktif (Streamlit)

Dashboard dapat diakses melalui link berikut:

🔗 https://bike-sharing-dashboardif210124069-aacyqyupeptfhia6zwryxe.streamlit.app/

Dashboard ini memungkinkan pengguna:
- Filter Tahun: Memilih data berdasarkan tahun, yaitu 2011 atau 2012
- Ringkasan Penyewaan: Menampilkan total penyewaan, rata-rata harian, dan hari dengan penyewaan tertinggi (angka berwarna)
- Tabs Interaktif:
  - Cuaca: Analisis rata-rata penyewaan sepeda berdasarkan kondisi cuaca
  - Pola Jam: Pola penyewaan per jam, dengan perbandingan weekday vs weekend
  - Heatmap: Visualisasi penyewaan berdasarkan jam dan hari dalam seminggu
  - Musim: Rata-rata penyewaan per musim
  - Clustering: Klasifikasi hari menjadi Sepi – Normal – Ramai
  - Tren Tahunan: Tren penyewaan dari tahun 2011 hingga 2012

Prediksi: Prediksi penyewaan 30 hari ke depan menggunakan Linear Regression
---

## Teknologi yang Digunakan

- Python
- Pandas
- Matplotlib
- Scikit-learn
- Streamlit

---

## Struktur Repository

- app.py: File utama yang dijalankan dengan streamlit run app.py
- Bike_Sharing_Analysis_IF2.ipynb: Notebook untuk eksplorasi data dan clustering
- day.csv & hour.csv: Dataset yang dipakai untuk analisis
- requirements.txt: File berisi daftar library Python (streamlit, pandas, numpy, plotly, scikit-learn, dll.)
- dashboard.png: Screenshot dashboard untuk README

---

## Video Demo

🔗 
