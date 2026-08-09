# 🛍️ StyleUp - AI Customer Service Chatbot

StyleUp Chatbot AI adalah aplikasi Customer Service (CS) digital berbasis web yang dibangun menggunakan **Streamlit** sebagai antarmuka pengguna dan **OpenRouter** (`nvidia/nemotron-3-nano-30b-a3b:free`) sebagai otak kecerdasan buatannya. Chatbot ini diprogram secara khusus dengan kepribadian bernama **"Siti"** yang ramah, informatif, dan patuh pada katalog produk toko fashion StyleUp.

## ✨ Fitur Utama
- **Kepribadian CS Khas ("Siti")**: Merespons dengan Bahasa Indonesia yang santun, kasual, dan ramah (menggunakan sapaan *Kak/Kakak* serta emoji yang relevan).
- **Katalog Produk Terintegrasi**: Siti hanya akan menjawab pertanyaan stok dan harga berdasarkan data asli toko StyleUp.
- **Proteksi Topik**: Menolak pertanyaan di luar topik fashion, gaya busana, dan belanja dengan halus.
- **Manajemen Riwayat Sesi**: Menyimpan riwayat obrolan selama sesi browser berlangsung menggunakan `st.session_state`.
- **Keamanan API Key**: Menggunakan konfigurasi aman `st.secrets` untuk mencegah kebocoran API Key ke publik.

## 🛠️ Prasyarat (Prerequisites)
Sebelum menjalankan proyek ini, pastikan Anda telah menginstal:
- Python 3.10 atau versi di atasnya
- API Key aktif dari [Open Router](https://openrouter.ai/)

## 🚀 Cara Menjalankan di Komputer Lokal

### 1. Kloning Repositori
```bash
git clone https://github.com
cd styleup-chatbot-cs
```
*(Catatan: Ganti USERNAME_ANDA/REPOSITORI_ANDA dengan tautan repositori GitHub Anda sendiri).*

### 2. Instal Dependensi
Pasang semua pustaka Python yang diperlukan yang terdaftar di `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi API Key (Penting & Rahasia)
Buat struktur folder dan file konfigurasi rahasia untuk menyimpan API Key Anda secara aman:
1. Buat folder bernama `.streamlit/` di direktori utama proyek Anda.
2. Di dalam folder tersebut, buat file bernama `secrets.toml`.
3. Isi file `secrets.toml` dengan format berikut:
   ```toml
   OPENROUTER_API_KEY = "MASUKKAN_API_OPEN ROUTER_ANDA"
   ```

> ⚠️ **PENTING**: File `.streamlit/secrets.toml` sudah dimasukkan ke dalam `.gitignore` sehingga aman dan tidak akan pernah ikut terunggah ke repositori GitHub publik Anda.

### 4. Jalankan Aplikasi
Jalankan server lokal Streamlit Anda dengan perintah:
```bash
streamlit run app.py
```
Aplikasi otomatis akan terbuka di browser Anda pada alamat default `http://localhost:8501`.

## 📦 Struktur Direktori Proyek
```text
styleup-chatbot-cs/
│
├── .streamlit/
│   └── secrets.toml      # Menyimpan API Key (DILINDUNGI / LOKAL SAJA)
│
├── app.py                # Kode utama aplikasi Chatbot Streamlit
├── .gitignore            # Daftar file yang diabaikan oleh Git (Mengamankan secrets.toml)
├── requirements.txt      # Daftar pustaka Python (Streamlit & Google GenAI)
└── README.md             # Dokumentasi proyek (File ini)
```

## 📜 Lisensi
Proyek ini dibuat untuk keperluan pembelajaran dan pengembangan chatbot AI menggunakan Open Router API.

## Demo 
Link Demo:[https://chatbot-xdpwmm2snbqlywrjzrpq2m.streamlit.app/]