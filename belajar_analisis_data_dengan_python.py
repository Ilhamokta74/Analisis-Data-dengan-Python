# -*- coding: utf-8 -*-
"""Belajar Analisis Data dengan Python.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1V2VmQHlKmpVhGTIlDNE35XQMjmYmi_4e

# Proyek Analisis Data: Bike-sharing-dataset
- **Nama : Ilham Oktavian**
- **Email : ilhamoktavian74@gmail.com**
- **ID Dicoding : ilham_oktavian_74**

## Menentukan Pertanyaan Bisnis

- Pertanyaan 1 : Berapa total terpinjam pada bulan Desember 2012?
- Pertanyaan 2 : Bagaimana kinerja peminjaman dalam setahun terakhir?

### Connect to Google Drive
"""

from google.colab import drive
drive.mount('/content/drive')

"""## Import Semua Packages/Library yang Digunakan"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

"""## Data Wrangling

### Gathering Data
"""

url = '/content/drive/MyDrive/Dataset/day.csv'  # Path ke file CSV
day = pd.read_csv(url)  # Membaca file CSV ke dalam DataFrame

day  # Menampilkan DataFrame

url2 = '/content/drive/MyDrive/Dataset/hour.csv'  # Path ke file CSV
hour = pd.read_csv(url2)  # Membaca file CSV ke dalam DataFrame

hour  # Menampilkan DataFrame

q = hour.groupby('dteday')['cnt'].sum().reset_index()  # Mengelompokkan data berdasarkan 'dteday', menjumlahkan 'cnt', dan mengatur ulang indeks
q  # Menampilkan DataFrame hasil

"""### Assessing Data"""

hour.info()

"""Perbedaan dataset day dan hour adalah dataset day adalah akumulasi dari dataset hour. Berikut merupakan penjelasan tiap kolom:
* instant: indeks
* dteday : tanggal peminjaman sepeda
* season : musim ketika peminjaman sepeda dilakukan. Musim dingin (1), musim semi (2), musim panas (3), musim gugur (4)
* yr : tahun. 2011 (0), 2012 (1)
* mnth : bulan, 1 sampai 12
* hr : jam, 1 hari 24 jam (0 hingga 23)
* holiday :  indikator yang menunjukkan apakah hari itu merupakan hari libur atau tidak
* weekday : hari dalam seminggu
* workingday : indikator yang jika hari tersebut bukan akhir pekan atau hari libur maka nilainya 1, jika tidak maka nilainya 0
* weathersit : kondisi cuaca pada saat peminjaman sepeda dilakukan. Cerah (1), Mendung (2), Hujan atau salju ringan (3), Hujan Lebat (4)
* temp :   suhu dalam derajat Celsius pada saat peminjaman sepeda dilakukan
* atemp: suhu yang dirasakan dalam derajat Celsius pada saat peminjaman sepeda dilakukan
* hum: Kelembapan
* windspeed: Kecepatan angin
* casual: jumlah peminjam sepeda biasa, yang tidak  berlangganan tetap
* registered: jumlah peminjam sepeda yang terdaftar member
* cnt: total jumlah peminjam sepeda, yaitu gabungan dari jumlah peminjam casual dan peminjam terdaftar
"""

print("Jumlah entri untuk setiap kolom dalam data hour:")
hour.nunique()

hour.isna().sum()

"""tidak ada missing values dalam setiap kolom"""

hour.duplicated().sum()

"""tidak ada data yang duplikat"""

hour.describe()

"""### Cleaning Data

**outliers**
"""

# Menghitung kuartil pertama (Q1) dan kuartil ketiga (Q3) dari kolom 'cnt'
Q1 = hour['cnt'].quantile(0.25)
Q3 = hour['cnt'].quantile(0.75)

# Menghitung rentang interkuartil (IQR)
IQR = Q3 - Q1

# Menentukan batas maksimum dan minimum untuk mendeteksi outlier
maximum = Q3 + (1.5 * IQR)
minimum = Q1 - (1.5 * IQR)

# Mengidentifikasi nilai yang kurang dari batas minimum (outlier bawah)
kondisi_lower_than = hour['cnt'] < minimum

# Mengidentifikasi nilai yang lebih dari batas maksimum (outlier atas)
kondisi_more_than = hour['cnt'] > maximum

# Menghitung jumlah nilai outlier
jumlah_outlier = kondisi_lower_than.sum() + kondisi_more_than.sum()

print(jumlah_outlier)  # Menampilkan jumlah nilai outlier

"""karena jumlah outlier hanya sedikit jadi bisa langsung didrop"""

# Menghapus baris yang memiliki nilai kurang dari batas minimum (outlier bawah)
hour.drop(hour[kondisi_lower_than].index, inplace=True)

# Menghapus baris yang memiliki nilai lebih dari batas maksimum (outlier atas)
hour.drop(hour[kondisi_more_than].index, inplace=True)

# Menampilkan DataFrame setelah penghapusan outlier
hour

"""**Memperbaiki tipe data**"""

hour['dteday'] = pd.to_datetime(hour['dteday'])

hour.info()

"""## Exploratory Data Analysis (EDA)"""

# Mengelompokkan data berdasarkan bulan dan menjumlahkan nilai 'cnt' untuk setiap bulan
bulanan = hour.groupby(pd.Grouper(key='dteday', freq='M')).sum()

# Membuat grafik
plt.figure(figsize=(10, 3))  # Menetapkan ukuran grafik
plt.plot(bulanan.index, bulanan['cnt'], marker='o', linestyle='-')  # Plot data dengan marker bulat dan garis
plt.title('Jumlah Penyewaan Sepeda per Bulan (Jan 2011 - Des 2012)')  # Menambahkan judul grafik
plt.xlabel('Bulan')  # Menambahkan label sumbu x
plt.ylabel('Jumlah Penyewaan')  # Menambahkan label sumbu y
plt.grid(True)  # Menambahkan grid ke grafik
plt.show()  # Menampilkan grafik

import plotly.express as px  # Pastikan Anda telah mengimpor plotly.express

# Daftar fitur yang akan dianalisis
fitur = ['mnth', 'hr', 'weekday', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered']

# Loop untuk membuat histogram untuk setiap fitur
for feature in fitur:
    # Membuat histogram menggunakan Plotly Express
    fig = px.histogram(hour, x=feature, y='cnt', title=f'Distribusi {feature}')

    # Menambahkan garis tepi hitam pada batang histogram
    fig.update_traces(marker_line_color='black', marker_line_width=1)

    # Menambahkan label pada sumbu y
    fig.update_layout(yaxis_title='Jumlah peminjam')

    # Menampilkan histogram
    fig.show()

import plotly.express as px  # Pastikan Anda telah mengimpor plotly.express

# Daftar fitur untuk analisis pie chart
w = ['yr', 'holiday', 'workingday', 'weathersit']

# Loop untuk membuat pie chart untuk setiap fitur
for feature in w:
    # Membuat pie chart menggunakan Plotly Express
    fig = px.pie(hour, names=feature, values='cnt',
                 title=f'Distribusi Jumlah Penyewaan Berdasarkan {feature}')

    # Menampilkan pie chart
    fig.show()

# Menghitung matriks korelasi untuk semua kolom numerik dalam DataFrame
matrikskorelasi = hour.corr()

# Membuat heatmap dari matriks korelasi
plt.figure(figsize=(9, 6))  # Menetapkan ukuran gambar
sns.heatmap(matrikskorelasi, annot=True, annot_kws={"size": 6}, cmap='coolwarm', center=0)
plt.title('Korelasi Antar Kolom')  # Menambahkan judul heatmap
plt.show()  # Menampilkan heatmap

"""## Visualization & Explanatory Analysis

### Pertanyaan 1: Berapa total terpinjam pada bulan Desember 2012?
"""

# Memfilter data untuk bulan Desember 2012
data_december_2012 = hour[(hour['yr'] == 1) & (hour['mnth'] == 12)]

# Membuat grafik batang untuk bulan Desember 2012
plt.figure(figsize=(12, 6))  # Menetapkan ukuran grafik
plt.bar(data_december_2012['dteday'], data_december_2012['cnt'], color='skyblue')  # Grafik batang dengan warna latar belakang
plt.title('Jumlah Penyewaan Sepeda pada Desember 2012')  # Menambahkan judul grafik
plt.xlabel('Tanggal')  # Menambahkan label sumbu x
plt.ylabel('Jumlah Penyewaan')  # Menambahkan label sumbu y
plt.grid(True, axis='y', linestyle='--', alpha=0.7)  # Menambahkan grid pada sumbu y
plt.xticks(rotation=45)  # Memutar label sumbu x untuk keterbacaan yang lebih baik
plt.tight_layout()  # Menyesuaikan tata letak untuk mencegah pemotongan
plt.show()  # Menampilkan grafik

# Menghitung total jumlah penyewaan sepeda pada bulan Desember 2012
total = data_december_2012['cnt'].sum()
print("\n Total terpinjam pada bulan Desember 2012:", total)

"""### Pertanyaan 2: Bagaimana kinerja peminjaman dalam setahun terakhir?"""

# Filter data untuk tahun yang relevan (misalnya, tahun 2012 jika 'yr' == 1)
data = hour[hour['yr'] == 1]

# Mengelompokkan data berdasarkan bulan dan menjumlahkan jumlah penyewaan
bulan = data.groupby(pd.Grouper(key='dteday', freq='M')).sum()

# Membuat grafik
plt.figure(figsize=(10, 3))  # Menetapkan ukuran grafik
plt.plot(bulan.index, bulan['cnt'], marker='o', linestyle='-')  # Plot data dengan marker bulat dan garis
plt.xticks(bulan.index, bulan.index.strftime('%b'))  # Mengatur label sumbu x untuk menampilkan nama bulan
plt.title('Kinerja Peminjaman dalam Setahun Terakhir')  # Menambahkan judul grafik
plt.xlabel('Bulan')  # Menambahkan label sumbu x
plt.ylabel('Jumlah Penyewaan')  # Menambahkan label sumbu y
plt.grid(True)  # Menambahkan grid ke grafik
plt.show()  # Menampilkan grafik

"""## Conclusion

- Conclution pertanyaan 1: Total sepeda terpinjam pada bulan Desember 2012 yaitu 114.538
- Conclution pertanyaan 2: dari bulan januari hingga mei peminjaman sepeda terus meningkat, sempat turun sedikit pada bulan juni, namun naik kembali pada bulan juli (pada bulan ini tercapai peminjaman terbanyak pada tahun 2012), namun setelah bulan juli jumlah peminjaman sepeda mengalami penurunan hingga akhir tahun 2012
- Berdasarkan matriks korelasi didapatkan faktor yang paling berpengaruh yaitu jam peminjaman. Dan berdasarkan distribusinya, sepeda paling sering dipinjam pada pukul 4 sore hingga 7 malam
"""

