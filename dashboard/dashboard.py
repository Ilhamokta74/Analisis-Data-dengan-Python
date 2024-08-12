import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px

# Setup Streamlit
st.title('Proyek Analisis Data: Bike Sharing')
st.markdown("""
- **Nama:** Ilham Oktavian
- **Email:** ilhamoktavian74@gmail.com
- **ID Dicoding:** ilham_oktavian_74
""")

# Load data
hour = pd.read_csv('hour.csv')
hour['dteday'] = pd.to_datetime(hour['dteday'])  # Pastikan kolom tanggal diproses dengan benar

# Clean data
Q1 = hour['cnt'].quantile(0.25)
Q3 = hour['cnt'].quantile(0.75)
IQR = Q3 - Q1
maximum = Q3 + (1.5 * IQR)
minimum = Q1 - (1.5 * IQR)
hour = hour[(hour['cnt'] >= minimum) & (hour['cnt'] <= maximum)]

# Plot function for monthly data
def plot_monthly(data):
    bulanan = data.groupby(pd.Grouper(key='dteday', freq='M')).sum()
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(bulanan.index, bulanan['cnt'], marker='o', linestyle='-', color='skyblue')
    ax.set_xticks(bulanan.index)
    ax.set_xticklabels(bulanan.index.strftime('%b'), color='white')
    ax.set_yticklabels(ax.get_yticks(), color='white')
    ax.set_xlabel('Bulan', color='white')
    ax.set_ylabel('Jumlah Penyewaan', color='white')
    ax.grid(True, color='white')
    ax.set_facecolor('#00172B') 
    fig.patch.set_facecolor('#00172B') 
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    st.pyplot(fig)

# Main function
def main():
    st.subheader("Jumlah Penyewaan Sepeda per Bulan (Jan 2011 - Des 2012)")
    plot_monthly(hour)

if __name__ == "__main__":
    main()

# Distribusi berdasarkan kategori
st.subheader('Distribusi Jumlah Penyewaan Berdasarkan Tiap Kategori')
fitur = ['mnth', 'hr', 'weekday', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered']
for feature in fitur:
    fig = px.histogram(hour, x=feature, y='cnt', title=f'Distribusi {feature}')
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    fig.update_layout(yaxis_title='Jumlah peminjam')
    st.plotly_chart(fig)

categories = ['yr', 'holiday', 'workingday', 'weathersit']
def show_pie_charts(categories):
    for category in categories: 
        fig = px.pie(hour, names=category, values='cnt', title=f'Distribusi Jumlah Penyewaan Berdasarkan {category}')
        st.plotly_chart(fig)
show_pie_charts(categories)

# Korelasi antar kolom
st.subheader('Korelasi Antar Kolom')
matrikskorelasi = hour.corr()
fig, ax = plt.subplots(figsize=(9, 6), facecolor='#00172B')
heatmap = sns.heatmap(matrikskorelasi, annot=True, annot_kws={"size": 5}, ax=ax, linewidths=.5, cmap='coolwarm', center=0)
heatmap.set_xticklabels(heatmap.get_xticklabels(), color='white')
heatmap.set_yticklabels(heatmap.get_yticklabels(), color='white')
st.pyplot(fig)

# Pertanyaan Bisnis
st.header('Pertanyaan Bisnis')
st.markdown("""
- Pertanyaan 1: Berapa total terpinjam pada bulan Desember 2012?
- Pertanyaan 2: Bagaimana kinerja peminjaman dalam setahun terakhir?
""")


def plot_harian_streamlit(data):
    # Menyiapkan grafik
    fig, ax = plt.subplots(figsize=(10, 3))
    
    # Membuat grafik batang harian
    ax.bar(data['dteday'], data['cnt'], color='wheat')
    
    # Menetapkan elemen-elemen pada grafik
    ax.set_xticks(data['dteday'])
    ax.set_xticklabels(data['dteday'].dt.strftime('%d'), color='white', rotation=45)
    ax.set_yticklabels(ax.get_yticks(), color='white')
    ax.set_xlabel('Tanggal', color='white')
    ax.set_ylabel('Jumlah Penyewaan', color='white')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7, color='white')
    
    # Menetapkan warna latar belakang dan garis tepi
    ax.set_facecolor('#00172B') 
    fig.patch.set_facecolor('#00172B') 
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)


def plot_bulanan_streamlit(data):
    bulan = data.groupby(pd.Grouper(key='dteday', freq='M')).sum()
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(bulan.index, bulan['cnt'], marker='o', linestyle='-', color='white')
    ax.set_xticks(bulan.index)
    ax.set_xticklabels(bulan.index.strftime('%b'), color='white')
    ax.set_yticklabels(ax.get_yticks(), color='white')
    ax.set_xlabel('Bulan', color='white')
    ax.set_ylabel('Jumlah Penyewaan', color='white')
    ax.grid(True, color='white')
    ax.set_facecolor('#00172B') 
    fig.patch.set_facecolor('#00172B') 
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    st.pyplot(fig)

def main():
    st.subheader("Total terpinjam pada bulan Desember 2012")
    plot_harian_streamlit(hour[(hour['yr'] == 1) & (hour['mnth'] == 12)])
    total = hour[(hour['yr'] == 1) & (hour['mnth'] == 12)]['cnt'].sum()  # Mengubah bulan ke Desember (11)
    st.write("Total terpinjam pada bulan Desember 2012:", total)

    st.subheader("Kinerja Peminjaman dalam Setahun Terakhir")
    plot_bulanan_streamlit(hour[hour['yr'] == 1])

if __name__ == "__main__":
    main()

# Conclusion
st.header("Conclusion")
st.markdown("""
- Total sepeda terpinjam pada bulan Desember 2012 yaitu 114.538
- Bulan Januari hingga Mei peminjaman sepeda mengalami peningkatan, sedikit mengalami penurunan pada bulan Juni, namun naik kembali pada bulan Juli (bulan dengan peminjaman terbanyak pada tahun 2012), setelah itu jumlah peminjaman mengalami penurunan hingga akhir tahun 2012
- Berdasarkan matriks korelasi, faktor yang paling berpengaruh adalah jam peminjaman. Berdasarkan distribusi, sepeda paling sering dipinjam pada pukul 4 sore hingga 7 malam
""")
