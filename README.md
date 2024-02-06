# IF-4-10121124
Tugas Besar Pemograman Basis Data

# Streamlit App

## Deskripsi Singkat
Streamlit adalah framework Python yang memungkinkan Anda membuat aplikasi web dengan cepat hanya dengan menggunakan script Python. Dengan Streamlit, Anda dapat membuat visualisasi data interaktif, dashboard, dan aplikasi web tanpa perlu pengetahuan mendalam tentang pengembangan web.

## Persiapan Lingkungan
Pastikan Anda memiliki Python terinstal di komputer Anda. Jika belum, unduh dan instal Python dari [https://www.python.org/](https://www.python.org/).

## Penggunaan
### 1. Clone Repository
```bash
git clone <URL_REPOSITORY>
# atau download manual dari https://github.com/<USERNAME>/<REPOSITORY_NAME>
```

### 2. Install Dependencies
Masuk ke direktori aplikasi dan instal semua modul yang diperlukan yang terdaftar dalam file requirements.txt.
```bash
cd <lokasi_folder>
pip install -r requirements.txt
```

### 3. Import Database
buat database dengan nama "db_pegawai"
```bash
cmd : create database db_pegawai
```
lalu gunakan database tadi
```bash
cmd : use database db_pegawai
```
Untuk mengimpor basis data, Anda dapat menggunakan perintah berikut jika menggunakan file SQL:
```bash
cmd : source path/to/your/file.sql
```
atau, jika Anda menggunakan phpMyAdmin, gunakan fitur "Import" untuk mengimpor basis data.

### 4. Menjalankan Streamlit
```bash
cd <lokasi_folder>
streamlit run main.py
```

Terimakasih atas perhatiannya



