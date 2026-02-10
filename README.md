# Bike Sharing Data Analysis 
![Dashboard Preview](dashboard.png)

Proyek ini berisi analisis data Bike Sharing untuk melihat pola penyewaan sepeda berdasarkan kondisi cuaca, musim, waktu, dan tren tahunan.
Hasil analisis ditampilkan dalam bentuk dashboard interaktif menggunakan Streamlit.

---

## Anggota Kelompok IF2

| NIM | Nama | Informasi Pekerjaan |
|-----|------|------|
| 10123318 | Jorge Fielnero Sauman | | 
| 10124051 | Raden Rama Feryl Alfaro | | 
| 10124064 | M. Rifqi Afriza Fasha | | 
| 10124069 | Deni Solehudin | | 
| 10124070 | Fazri Hariri | | 

---

## Latar Belakang

Data penyewaan sepeda dapat digunakan untuk memahami kebiasaan pengguna serta faktor-faktor yang memengaruhi tingkat permintaan. Dengan melakukan analisis terhadap data historis, dapat diketahui pola penyewaan berdasarkan waktu, kondisi cuaca, dan musim tertentu. Hasil analisis ini diharapkan dapat memberikan gambaran umum mengenai karakteristik penggunaan sepeda dari waktu ke waktu.

---
## Rumusan Masalah

Berdasarkan latar belakang tersebut, analisis ini difokuskan untuk menjawab beberapa permasalahan berikut:
1. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?
2. Pada jam berapa penyewaan sepeda paling tinggi, serta bagaimana perbedaannya antara hari kerja dan akhir pekan?
3. Musim apa yang memiliki jumlah penyewaan sepeda tertinggi?
4. Faktor lingkungan apa yang paling memengaruhi jumlah penyewaan sepeda?
5. Apakah terdapat tren peningkatan penggunaan sepeda dari tahun 2011 ke tahun 2012?

---

## Tahapan Analisis Data

Tahapan analisis data yang dilakukan meliputi:

- Data wrangling, yang mencakup proses pengumpulan dan pembersihan data
- Exploratory Data Analysis (EDA) untuk melihat pola awal pada data
- Visualisasi data untuk mempermudah interpretasi hasil analisis
- Penerapan algoritma K-Means Clustering untuk mengelompokkan hari berdasarkan tingkat penyewaan
- Pembuatan dashboard interaktif menggunakan Streamlit

Notebook analisis lengkap tersedia dalam file .ipynb pada repository ini.

---

## Hasil Analisis

Berdasarkan analisis data yang telah dilakukan, diperoleh beberapa hasil sebagai berikut:

- Jumlah penyewaan sepeda tertinggi terjadi pada kondisi cuaca cerah
- Pada hari kerja terdapat dua puncak penyewaan, yaitu pada pagi dan sore hari, sedangkan pada akhir pekan puncak terjadi pada siang hari
- Musim Summer dan Fall memiliki jumlah penyewaan sepeda yang lebih tinggi dibandingkan musim lainnya
- Suhu merupakan faktor lingkungan yang paling berpengaruh terhadap jumlah penyewaan sepeda
- Terjadi peningkatan jumlah penyewaan sepeda dari tahun 2011 ke tahun 2012
- Hasil clustering menunjukkan adanya perbedaan pola hari sepi, normal, dan ramai berdasarkan kondisi lingkungan

---

## Dashboard Interaktif

Dashboard dapat diakses melalui link berikut:

https://bike-sharing-dashboardif210124069-aacyqyupeptfhia6zwryxe.streamlit.app/

Dashboard ini menyediakan beberapa fitur, antara lain:

- Filter data berdasarkan tahun
- Ringkasan statistik penyewaan sepeda
- Visualisasi penyewaan berdasarkan cuaca, jam, dan musim
- Heatmap penyewaan berdasarkan jam dan hari
- Hasil clustering
- Tren penyewaan tahunan
- Prediksi penyewaan 30 hari ke depan

---

## Teknologi yang Digunakan

- Python
- Pandas
- Matplotlib
- Scikit-learn
- Streamlit

---

## Struktur Repository

- app.py – File utama untuk menjalankan dashboard Streamlit
- Bike_Sharing_Analysis_IF2.ipynb – Notebook analisis data dan clustering
- day.csv dan hour.csv – Dataset yang digunakan
- requirements.txt – Daftar library yang diperlukan
- README.md – Dokumentasi proyek
- dashboard.png – Tampilan dashboard

---

## Video Presentasi

Video dapat diakses melalui link berikut:


