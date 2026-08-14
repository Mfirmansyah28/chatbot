# 🛍️ StyleUp - AI Customer Service Chatbot

StyleUp Chatbot adalah aplikasi Customer Service digital berbasis web yang dibangun dengan **Streamlit** dan **OpenRouter** (`nvidia/nemotron-3-nano-30b-a3b:free`). Chatbot ini memiliki kepribadian bernama **"Siti"** — CS virtual StyleUp yang ramah, informatif, dan hanya menjawab seputar produk serta layanan toko fashion StyleUp.

## ✨ Fitur Utama

- **Kepribadian CS "Siti"** — Merespons dalam Bahasa Indonesia yang santun dan kasual, menggunakan sapaan *Kak/Kakak* dan emoji yang relevan.
- **Deteksi Intent Otomatis** — Mengenali intent pelanggan seperti pencarian produk, tanya harga, stok, pemesanan, pembayaran, pengiriman, retur, dan greeting.
- **Pencarian Produk Cerdas** — Mencari produk berdasarkan nama, warna, budget, dan preferensi harga dari katalog StyleUp.
- **Konteks Percakapan** — Memahami pertanyaan lanjutan seperti *"yang tadi berapa?"* atau *"ada warna lain?"* tanpa perlu mengulang informasi.
- **Guardrail Topik** — Menolak pertanyaan di luar topik fashion, belanja, dan layanan StyleUp secara halus.
- **Manajemen Multi-Chat** — Mendukung beberapa sesi chat dengan fitur buat, pilih, dan hapus riwayat chat.
- **Riwayat Chat Persisten** — Menyimpan riwayat obrolan ke `data/chats.json` sehingga tidak hilang saat halaman di-refresh.
- **Streaming Response** — Jawaban AI ditampilkan secara real-time token demi token.
- **Salin Jawaban** — Tombol Copy Response untuk menyalin jawaban AI dengan mudah.
- **Keamanan API Key** — Menggunakan `st.secrets` agar API Key tidak bocor ke publik.

## 🗂️ Struktur Direktori

```
chatbot/
│
├── .streamlit/
│   └── secrets.toml          # API Key (LOKAL SAJA, tidak di-commit)
│
├── data/
│   └── chats.json            # Penyimpanan riwayat chat
│
├── services/
│   ├── catalog.py            # Katalog produk, FAQ, dan system prompt Siti
│   ├── chat_manager.py       # CRUD manajemen sesi chat (JSON)
│   ├── conversation_context.py  # Membangun konteks percakapan sebelumnya
│   ├── guardrail.py          # Filter topik dan pesan penolakan
│   ├── intent.py             # Deteksi intent pelanggan
│   ├── intent_context.py     # Instruksi AI berdasarkan intent
│   ├── openrouter.py         # Client OpenRouter (streaming)
│   └── product_search.py     # Pencarian produk berdasarkan warna, budget, nama
│
├── ui/
│   └── sidebar.py            # Sidebar: New Chat, daftar, dan hapus chat
│
├── app.py                    # Entry point aplikasi Streamlit
├── requirements.txt          # Dependensi Python
├── runtime.txt               # Versi Python untuk deployment
├── .gitignore
└── README.md
```

## 📦 Katalog Produk

| Produk | Warna | Ukuran | Harga |
|---|---|---|---|
| Kemeja Flanel Kotak-Kotak | Merah-Hitam, Biru-Navy | M, L, XL | Rp 150.000 |
| Kaos Polos Katun Premium | Hitam, Putih, Sage Green, Lilac | S, M, L, XL | Rp 75.000 |
| Celana Chino Slimfit | Krem, Hitam, Abu-abu | 28, 30, 32, 34 | Rp 200.000 |

## 🛠️ Prasyarat

- Python 3.11
- API Key dari [OpenRouter](https://openrouter.ai/)

## 🚀 Menjalankan di Lokal

### 1. Clone Repositori

```bash
git clone https://github.com/USERNAME/chatbot.git
cd chatbot
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key

Buat file `.streamlit/secrets.toml` dan isi dengan:

```toml
OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxx"
```

> ⚠️ File `secrets.toml` sudah masuk `.gitignore` dan tidak akan ikut ter-commit ke GitHub.

### 5. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`.

## ⚙️ Cara Kerja

```
Input Pengguna
     │
     ▼
Guardrail (apakah topik relevan?)
     │  Tidak → Pesan penolakan Siti
     │  Ya ↓
     ▼
Deteksi Intent (greeting / product_search / payment / dst.)
     │
     ▼
Bangun Konteks (riwayat percakapan + instruksi intent + guardrail)
     │
     ▼
Product Search (jika intent = product_search)
     │
     ▼
Kirim ke OpenRouter (streaming)
     │
     ▼
Tampilkan Jawaban Siti + Simpan ke chats.json
```

## 🧰 Teknologi

| Komponen | Detail |
|---|---|
| Framework UI | Streamlit 1.46.1 |
| AI Provider | OpenRouter |
| Model AI | `nvidia/nemotron-3-nano-30b-a3b:free` |
| Client API | openai 1.99.9 (kompatibel OpenRouter) |
| Penyimpanan Chat | JSON lokal (`data/chats.json`) |
| Runtime | Python 3.11 |

## 🌐 Demo

[https://chatbot-xdpwmm2snbqlywrjzrpq2m.streamlit.app/]

## 📜 Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan pengembangan chatbot AI menggunakan OpenRouter API.
