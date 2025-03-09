import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat dan menggabungkan dataset
@st.cache_data  # Mengganti st.cache dengan st.cache_data
def load_data():
    # Memuat dataset Aotizhongxin, Changping, Dingling
    df_all = pd.read_csv("clean_df_all.csv")
    return df_all

# Panggil fungsi untuk memuat data
df_all = load_data()

# Fungsi untuk analisis satu
def run_analysis_one():
    st.title("Bagaimana pengaruh kecepatan angin (WSPM) terhadap penyebaran konsentrasi PM2.5 selama musim Panas (juni hingga agustus)?")
    if df_all.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        st.subheader("Hubungan Kecepatan Angin dengan Persebaran PM2.5")
        df_all['month'] = df_all['date_time'].dt.month
        dry_season_data = df_all[df_all['month'].isin([6, 7, 8])]
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x='WSPM', y='PM2.5', data=dry_season_data)
        plt.title('Hubungan Kecepatan Angin (WSPM) dengan PM2.5 Selama Musim Kemarau (Juni hingga Agustus)')
        plt.xlabel('Kecepatan Angin (WSPM)')
        plt.ylabel('Konsentrasi PM2.5')
        st.pyplot(plt)

def run_analysis_two():
    st.title("Bagaimana pengaruh konsentrasi NO2 dan CO sebagai polutan yang dihasilkan kendaraan bermotor terhadap kualitas udara ?")
    if df_all.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        st.subheader("Rata-rata Bulanan Konsentrasi Polutan")
        df_all['date_time_month'] = df_all['date_time'].dt.to_period('M')
        monthly_avg = df_all.groupby('date_time_month').agg({
            'CO': 'mean', 
            'NO2': 'mean',
            'PM2.5': 'mean',
            'PM10': 'mean',
            'SO2': 'mean',
            'O3': 'mean'
        }).reset_index()
        monthly_avg['date_time_month'] = monthly_avg['date_time_month'].dt.to_timestamp()
        plt.figure(figsize=(14, 8))
        sns.lineplot(x='date_time_month', y='CO', data=monthly_avg, label='CO', color='blue')
        sns.lineplot(x='date_time_month', y='NO2', data=monthly_avg, label='NO2', color='red')
        sns.lineplot(x='date_time_month', y='PM2.5', data=monthly_avg, label='PM2.5', color='green')
        sns.lineplot(x='date_time_month', y='PM10', data=monthly_avg, label='PM10', color='purple')
        sns.lineplot(x='date_time_month', y='SO2', data=monthly_avg, label='SO2', color='orange')
        sns.lineplot(x='date_time_month', y='O3', data=monthly_avg, label='O3', color='cyan')
        plt.title('Rata-rata Bulanan Konsentrasi Polutan')
        plt.xlabel('Bulan')
        plt.ylabel('Konsentrasi Polutan')
        plt.xticks(ticks=monthly_avg['date_time_month'], labels=monthly_avg['date_time_month'].dt.strftime('%Y-%m'), rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)

def run_analysis_three():
    st.title("Bagaimana pengaruh hujan terhadap polutan penyebab polusi udara?")
    if df_all.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        st.subheader("Bagaimana pengaruh hujan terhadap polutan penyebab polusi udara?")
        df_all['RAIN_GROUP'] = pd.cut(df_all['RAIN'], bins=[0, 1, 4, 8, 10], labels=['No Rain', 'Light Rain', 'Moderate Rain', 'Heavy Rain'])
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='RAIN_GROUP', y='PM2.5', data=df_all)
        plt.title('Boxplot of PM2.5 by Rain Intensity')
        plt.xticks(rotation=45)
        st.pyplot(plt)

def run_analysis_four():
    st.title("Bagaimana hubungan antara konsentrasi NO2, dan CO dengan pembentukan O3 ?")
    if df_all.empty:
        st.error("Data tidak tersedia. Pastikan file CSV telah dimuat dengan benar.")
    else:
        st.subheader("Konsentrasi NO2, CO, dan O3 Bulanan")
        df_all['date_time_month'] = df_all['date_time'].dt.to_period('M')
        monthly_avg = df_all.groupby('date_time_month').agg({'NO2': 'mean', 'CO': 'mean', 'O3': 'mean'}).reset_index()
        monthly_avg['date_time_month'] = monthly_avg['date_time_month'].dt.to_timestamp()
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='date_time_month', y='NO2', data=monthly_avg, label='NO2', color='red')
        sns.lineplot(x='date_time_month', y='CO', data=monthly_avg, label='CO', color='blue')
        sns.lineplot(x='date_time_month', y='O3', data=monthly_avg, label='O3', color='green')
        plt.title('Konsentrasi NO2, CO, dan O3 Bulanan')
        plt.xlabel('Bulan')
        plt.ylabel('Konsentrasi Polutan (NO2, CO, O3)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)

# Run all analyses
run_analysis_one()
run_analysis_two()
run_analysis_three()
run_analysis_four()
