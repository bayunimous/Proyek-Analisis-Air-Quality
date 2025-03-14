import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Menentukan direktori dasar berdasarkan lokasi file dashboard.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Air-quality-dataset")
IMAGE_PATH = os.path.join(BASE_DIR, "images", "logo.png")

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data():
    try:
        df_all_path = os.path.join(BASE_DIR, "clean_df_all.csv")
        if os.path.exists(df_all_path):
            df_all = pd.read_csv(df_all_path)
            df_all['date_time'] = pd.to_datetime(df_all['date_time'])
        else:
            df_all = None
            st.error(f"File {df_all_path} tidak ditemukan!")

        return df_all

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}")
        return None

# Memuat data
df_all = load_data()

# Menampilkan logo pada sidebar
if os.path.exists(IMAGE_PATH):
    st.sidebar.image(IMAGE_PATH)
else:
    st.sidebar.warning("Logo tidak ditemukan! Pastikan file 'logo.png' ada di folder 'images'.")

# Menu Navigasi
st.sidebar.title("Menu Navigasi")
menu = st.sidebar.selectbox("Pilih Menu:", ["Home", "Lihat Dataset", "Analisis Data", "Kesimpulan"])

if menu == "Home":
    st.title("Dashboard Analisis Kualitas Udara")
    st.write("Proyek Akhir Analisis Data: Air Quality Dataset")
    st.write("**Nama:** Bayu Nugraha (MC-03)")
    st.write("**Email:** bayunugraha.bjm@gmail.com")
    st.write("**Cohort ID:** MC216D5Y0488")

elif menu == "Lihat Dataset":
    if df_all is not None:
        st.subheader("Preview Dataset Utama")
        st.dataframe(df_all.head())
    else:
        st.error("Data tidak dapat dimuat. Pastikan semua file tersedia di lokasi yang benar.")

elif menu == "Analisis Data":
    if df_all is not None:
        min_date, max_date = df_all["date_time"].min(), df_all["date_time"].max()
        start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date])

        season_filter = st.sidebar.selectbox("Pilih Musim", ["Semua", "Winter", "Spring", "Summer", "Autumn"])
        
        # Hanya tampilkan pilihan filter kondisi cuaca jika kolom "weathersit" ada
        if "weathersit" in df_all.columns:
            weather_filter = st.sidebar.selectbox("Pilih Kondisi Cuaca", ["Semua", "Clear", "Cloudy", "Rainy"])
        else:
            weather_filter = "Semua"

        # Filter data berdasarkan tanggal
        df_filtered = df_all[(df_all["date_time"] >= pd.to_datetime(start_date)) & (df_all["date_time"] <= pd.to_datetime(end_date))]

        # Filter berdasarkan musim
        if season_filter != "Semua":
            season_map = {"Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8], "Autumn": [9, 10, 11]}
            df_filtered = df_filtered[df_filtered["date_time"].dt.month.isin(season_map[season_filter])]

        # Filter berdasarkan kondisi cuaca, hanya jika "weathersit" ada
        if weather_filter != "Semua" and "weathersit" in df_filtered.columns:
            weather_map = {"Clear": 1, "Cloudy": 2, "Rainy": 3}
            df_filtered = df_filtered[df_filtered["weathersit"] == weather_map[weather_filter]]

        st.subheader("Hasil Filter Data")
        st.write(df_filtered.head())

        # Visualisasi Bar Chart
        st.subheader("Rata-rata Konsentrasi Polutan Berdasarkan Filter")
        pollutant_avg = df_filtered[["NO2", "CO", "PM2.5"]].mean()

        plt.figure(figsize=(8, 5))
        sns.barplot(x=pollutant_avg.index, y=pollutant_avg.values, palette="coolwarm")
        plt.title("Rata-rata Konsentrasi NO2, CO, dan PM2.5")
        plt.ylabel("Konsentrasi")
        plt.show()
        st.pyplot(plt)

elif menu == "Kesimpulan":
    st.title("Kesimpulan")
    st.markdown("""
    **Kesimpulan dari Analisis Data:**
    1. **Kecepatan Angin (WSPM)** berperan dalam penyebaran polutan. Saat angin tinggi, PM2.5 menurun.
    2. **NO2 dan CO** meningkat karena aktivitas kendaraan bermotor.
    3. **Hujan** membantu menurunkan PM2.5 tetapi bisa meningkat dalam hujan lebat.
    4. **Konsentrasi NO2 dan CO** mempengaruhi pembentukan O3.
    """)
else:
    st.warning("Menu belum tersedia!")