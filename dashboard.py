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
menu = st.sidebar.selectbox("Pilih Menu:", ["Home", "Lihat Dataset", "Analisis Data", "Visualisasi", "Kesimpulan"])

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
        st.subheader("Analisis Data dengan Filter")

        # Fitur interaktif: Filtering berdasarkan tanggal
        min_date, max_date = df_all["date_time"].min(), df_all["date_time"].max()
        start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date])

        # Fitur interaktif: Filtering berdasarkan musim
        season_filter = st.sidebar.selectbox("Pilih Musim", ["Semua", "Winter", "Spring", "Summer", "Autumn"])
        
        # Fitur interaktif: Filtering berdasarkan kondisi cuaca
        if "weathersit" in df_all.columns:
            weather_filter = st.sidebar.selectbox("Pilih Kondisi Cuaca", ["Semua", "Clear", "Cloudy", "Rainy"])
        else:
            weather_filter = "Semua"

        # Menerapkan filter pada dataset
        df_filtered = df_all[(df_all["date_time"] >= pd.to_datetime(start_date)) & (df_all["date_time"] <= pd.to_datetime(end_date))]

        if season_filter != "Semua":
            season_map = {"Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8], "Autumn": [9, 10, 11]}
            df_filtered = df_filtered[df_filtered["date_time"].dt.month.isin(season_map[season_filter])]

        if weather_filter != "Semua" and "weathersit" in df_filtered.columns:
            weather_map = {"Clear": 1, "Cloudy": 2, "Rainy": 3}
            df_filtered = df_filtered[df_filtered["weathersit"] == weather_map[weather_filter]]

        # Menampilkan hasil filter dalam bentuk visualisasi
        st.subheader("Distribusi PM2.5 Setelah Filter Diterapkan")
        
        # Teks dinamis berdasarkan musim yang dipilih
        explanation = "**Apa yang ditampilkan?**\n\n"
        explanation += "- Histogram ini menunjukkan distribusi konsentrasi **PM2.5** setelah penerapan filter.\n"

        if season_filter == "Winter":
            explanation += "- Musim dingin sering kali memiliki **polusi lebih tinggi** karena udara dingin dapat menjebak polutan di dekat permukaan tanah.\n"
        elif season_filter == "Spring":
            explanation += "- Di musim semi, polusi udara cenderung **lebih rendah** karena hujan dan angin sering membersihkan udara.\n"
        elif season_filter == "Summer":
            explanation += "- Musim panas biasanya memiliki **variasi besar dalam PM2.5**, karena peningkatan suhu dapat meningkatkan reaksi kimia polutan tertentu.\n"
        elif season_filter == "Autumn":
            explanation += "- Pada musim gugur, PM2.5 bisa meningkat karena **aktivitas pertanian atau pembakaran biomassa**.\n"
        else:
            explanation += "- Semua musim ditampilkan, sehingga pola polusi sepanjang tahun dapat diamati.\n"

        st.markdown(explanation)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(df_filtered["PM2.5"], bins=30, kde=True, ax=ax)
        ax.set_xlabel("PM2.5 Concentration")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        st.subheader("Rata-rata PM2.5 Berdasarkan Musim")

        # Teks dinamis untuk rata-rata PM2.5 berdasarkan musim
        explanation_season = "**Apa yang ditampilkan?**\n\n"
        explanation_season += "- Grafik batang ini menunjukkan rata-rata **PM2.5** di setiap bulan berdasarkan filter yang dipilih.\n"

        if season_filter == "Winter":
            explanation_season += "- Pada musim dingin, rata-rata PM2.5 bisa lebih tinggi karena **kurangnya pergerakan udara**.\n"
        elif season_filter == "Spring":
            explanation_season += "- Musim semi sering menunjukkan **penurunan PM2.5** karena curah hujan dan angin yang lebih tinggi.\n"
        elif season_filter == "Summer":
            explanation_season += "- Di musim panas, PM2.5 bisa dipengaruhi oleh **aktivitas kendaraan dan peningkatan ozon**.\n"
        elif season_filter == "Autumn":
            explanation_season += "- Pada musim gugur, ada kemungkinan peningkatan PM2.5 karena **debu dan aktivitas pertanian**.\n"
        else:
            explanation_season += "- Semua musim ditampilkan, sehingga kita bisa melihat pola jangka panjang PM2.5 sepanjang tahun.\n"

        st.markdown(explanation_season)

        season_avg = df_filtered.groupby(df_filtered["date_time"].dt.month)["PM2.5"].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        season_avg.plot(kind='bar', color='blue', ax=ax)
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Rata-rata PM2.5")
        st.pyplot(fig)


elif menu == "Visualisasi":
    if df_all is not None:
        st.subheader("Visualisasi Data")

        # Pilihan visualisasi berdasarkan pertanyaan bisnis
        visual_option = st.selectbox("Pilih Visualisasi", ["Distribusi PM2.5", "Pengaruh Kecepatan Angin terhadap PM2.5"])

        if visual_option == "Distribusi PM2.5":
            st.subheader("Distribusi Konsentrasi PM2.5")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(df_all["PM2.5"], bins=30, kde=True, ax=ax)
            ax.set_xlabel("PM2.5 Concentration")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        elif visual_option == "Pengaruh Kecepatan Angin terhadap PM2.5":
            st.subheader("Rata-rata Konsentrasi PM2.5 Selama Musim Panas")
            df_all['month'] = df_all['date_time'].dt.month
            df_summer = df_all[df_all['month'].isin([6, 7, 8])]
            summer_agg = df_summer.groupby('month')[['WSPM', 'PM2.5']].mean().reset_index()

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(x=summer_agg['month'], y=summer_agg['PM2.5'], color="blue", ax=ax)
            ax.set_xlabel("Bulan")
            ax.set_ylabel("PM2.5")
            st.pyplot(fig)

elif menu == "Kesimpulan":
    st.title("Kesimpulan")
    st.markdown("""
    **Kesimpulan dari Analisis Data:**
    1. **Kecepatan Angin (WSPM) mempengaruhi PM2.5**  
       - Kecepatan angin yang lebih tinggi membantu menyebarkan polutan, sehingga konsentrasi PM2.5 menurun.  
       - Sebaliknya, saat kecepatan angin rendah, polusi udara cenderung menumpuk di satu area.  

    2. **Hubungan NO2, CO, dan PM2.5**  
       - Terdapat korelasi positif antara NO2 dan CO dengan PM2.5.  
       - Peningkatan NO2 dan CO sering terjadi pada jam-jam sibuk, mengindikasikan bahwa kendaraan bermotor merupakan sumber utama polusi udara.  
    """)
else:
    st.warning("Menu belum tersedia!")
