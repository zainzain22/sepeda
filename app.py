import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

data_url = "https://raw.githubusercontent.com/zainzain22/sepeda/refs/heads/main/day.csv"
df = pd.read_csv(data_url)

page = st.selectbox("Pilih halaman", ["Pertanyaan 1: Hubungan Season dan Cnt", "Pertanyaan 2: Hubungan Weekday dan Cnt"])

def display_table(data):
    st.write(data)

if page == "Pertanyaan 1: Hubungan Season dan Cnt":
    #visualisasi barplot pertanyaan 1
    st.subheader("Tabel Total Jumlah Sepeda yang Dipinjam Berdasarkan Musim (Season)")
    season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    df['season'] = df['season'].map(season_mapping)
    season_cnt_total = df.groupby('season')['cnt'].sum().reset_index()
    display_table(season_cnt_total)
    gradient_palette_season = sns.color_palette(["#003f5c", "#375a8c", "#7a8dbe", "#bcdef0"])
    st.subheader("Bar Plot untuk Total Jumlah Sepeda yang Dipinjam berdasarkan Musim")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=season_cnt_total, x='season', y='cnt', palette=gradient_palette_season)
    plt.title('Bar Plot - Total Jumlah Sepeda yang Dipinjam berdasarkan Musim', fontsize=16)
    plt.xlabel('Musim (Season)', fontsize=14)
    plt.ylabel('Total Jumlah Sepeda yang Dipinjam (cnt)', fontsize=14)
    plt.grid(True)
    st.pyplot(plt)

    #visualisasi boxplot pertanyaan 1
    st.subheader("Box Plot untuk Distribusi Jumlah Sepeda yang Dipinjam berdasarkan Musim")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='season', y='cnt', palette=gradient_palette_season)
    plt.title('Box Plot - Distribusi Jumlah Sepeda yang Dipinjam berdasarkan Musim', fontsize=16)
    plt.xlabel('Musim (Season)', fontsize=14)
    plt.ylabel('Jumlah Sepeda yang Dipinjam (cnt)', fontsize=14)
    plt.grid(True)
    st.pyplot(plt)

    # Bagian Binning
    bins = [0, 100, 200, 300, float('inf')]
    labels = ['Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']

    df['cnt_binned'] = pd.cut(df['cnt'], bins=bins, labels=labels, right=False)
    season_cnt_binned = df.groupby(['season', 'cnt_binned'])['cnt'].sum().unstack().fillna(0)
    st.subheader("Tabel Jumlah Sepeda yang Dipinjam Berdasarkan Musim dan Kategori")
    display_table(season_cnt_binned)

    # Visualisasi HEATMAP
    st.subheader("Heatmap Jumlah Sepeda yang Dipinjam Berdasarkan Musim dan Kategori")
    plt.figure(figsize=(10, 6))
    sns.heatmap(season_cnt_binned, annot=True, fmt=".0f", cmap='YlGnBu', linewidths=0.5)
    plt.title('Heatmap - Jumlah Sepeda yang Dipinjam Berdasarkan Musim dan Kategori')
    plt.xlabel('Kategori Jumlah Sepeda (cnt_binned)')
    plt.ylabel('Musim (Season)')
    st.pyplot(plt)

    # Kesimpulan
    st.write("""
    ### Kesimpulan:
    Berdasarkan heatmap di atas, kita dapat melihat distribusi jumlah sepeda yang dipinjam berdasarkan musim dan kategori bin:
    1. Musim panas (*Summer*) cenderung memiliki jumlah sepeda yang dipinjam dalam kategori tinggi dan sangat tinggi.
    2. Musim dingin (*Winter*) menunjukkan lebih banyak kategori rendah dalam hal peminjaman sepeda.
    """)

elif page == "Pertanyaan 2: Hubungan Weekday dan Cnt":
    st.subheader("Tabel Total Jumlah Sepeda yang Dipinjam Berdasarkan Hari (Weekday)")
    weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
    df['weekday'] = df['weekday'].map(weekday_mapping)
    ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['weekday'] = pd.Categorical(df['weekday'], categories=ordered_days, ordered=True)
    weekday_cnt_total = df.groupby('weekday')['cnt'].sum().reindex(ordered_days).reset_index()
    display_table(weekday_cnt_total)
    gradient_palette_weekday = sns.color_palette(["#004d00", "#006600", "#338a00", "#66b300"])

    # Visualisasi LINEPLOT pertanyaan 2
    st.subheader("Line Plot untuk Total Jumlah Sepeda yang Dipinjam berdasarkan Hari")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=weekday_cnt_total['weekday'], y=weekday_cnt_total['cnt'], marker='o', palette=gradient_palette_weekday, linewidth=2.5)
    plt.title('Line Plot - Total Jumlah Sepeda yang Dipinjam berdasarkan Hari', fontsize=16)
    plt.xlabel('Hari', fontsize=14)
    plt.ylabel('Total Jumlah Sepeda yang Dipinjam (cnt)', fontsize=14)
    plt.grid(True)
    st.pyplot(plt)

    # Visualisasi BOXPLOT pertanyaan 2
    st.subheader("Box Plot untuk Distribusi Jumlah Sepeda yang Dipinjam berdasarkan Weekday")
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='weekday', y='cnt', order=ordered_days)  # Menambahkan parameter 'order' untuk mengatur urutan hari
    plt.title('Box Plot - Distribusi Jumlah Sepeda yang Dipinjam berdasarkan Hari', fontsize=16)
    plt.xlabel('Hari', fontsize=14)
    plt.ylabel('Jumlah Sepeda yang Dipinjam (cnt)', fontsize=14)
    plt.grid(True)
    st.pyplot(plt)

    highest_cnt_day = weekday_cnt_total.loc[weekday_cnt_total['cnt'].idxmax(), 'weekday']
    st.write(f"Hari dengan total jumlah sepeda tertinggi adalah: {highest_cnt_day}")
    st.write(f"""
    ### Kesimpulan:
    Dari visualisasi di atas, kita bisa melihat pola total jumlah sepeda yang dipinjam berdasarkan hari (weekday):
    1. **Line Plot** memperlihatkan tren total jumlah sepeda yang dipinjam untuk setiap hari dalam seminggu.
    2. **Box Plot** memperlihatkan distribusi jumlah sepeda yang dipinjam setiap hari.
    3. **Kesimpulan akhir** menunjukkan bahwa hari dengan total peminjaman sepeda tertinggi adalah {highest_cnt_day}.
    """)

