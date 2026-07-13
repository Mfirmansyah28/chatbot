import streamlit as st
from google import genai
from google.genai import types

# 1. Mengambil API Key secara aman dari secrets.toml
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Error: API Key tidak ditemukan. Pastikan file .streamlit/secrets.toml sudah dibuat dengan benar.")
    st.stop()

# 2. Masukkan System Instructions & Katalog Toko
system_instruction = """
Kamu adalah "Siti", seorang agen Customer Service digital yang cerdas, ramah, dan solutif dari toko fashion "StyleUp". 
Tugas utamanya adalah menyapa pelanggan, menjawab pertanyaan seputar produk pakaian, dan membantu proses belanja dengan santun.

Aturan yang WAJIB kamu patuhi:
1. Gunakan Bahasa Indonesia yang ramah dan kasual, gunakan panggilan "Kak" atau "Kakak" kepada pelanggan.
2. Selalu gunakan emoji yang relevan agar terkesan ramah (seperti 😊,🛍️,✨).
3. Jika pelanggan bertanya hal di luar topik toko fashion, belanja, atau gaya berpakaian, tolak dengan halus dan ingatkan kembali tugasmu sebagai CS StyleUp.
4. JAWABLAH PERTANYAAN STOK DAN HARGA HANYA BERDASARKAN DATA DI BAWAH INI. Jika tidak ada di data, katakan stok sedang kosong atau belum tersedia.

=== DATA KATALOG PRODUK STYLEUP ===
1. Kemeja Flanel Kotak-Kotak (Merah-Hitam, Biru-Navy) | M, L, XL | Rp 150.000
2. Kaos Polos Katun Premium (Hitam, Putih, Sage Green, Lilac) | S, M, L, XL | Rp 75.000
3. Celana Chino Slimfit (Krem, Hitam, Abu-abu) | 28, 30, 32, 34 | Rp 200.000
"""

# 3. Setup Halaman Tampilan Web Streamlit
st.set_page_config(page_title="StyleUp Chatbot CS", page_icon="🛍️")
st.title("🛍️ StyleUp - AI Customer Service")
st.write("Halo! Selamat datang di StyleUp. Ada yang bisa Siti bantu hari ini?")

# 4. Inisialisasi Client
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=API_KEY)

# 5. Inisialisasi Chat Session dengan Model Terbaru & Stabil
if "chat_session_v2" not in st.session_state:
    try:
        st.session_state.chat_session_v2 = st.session_state.client.chats.create(
            model="gemini-2.0-flash", 
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
    except Exception as e:
        st.error(f"Gagal menghubungkan ke AI Gemini: {e}")

# 6. Tampilkan Riwayat Obrolan
if "chat_session_v2" in st.session_state:
    for message in st.session_state.chat_session_v2.get_history():
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.write(message.parts[0].text)

# 7. Kotak Input Chat
if user_input := st.chat_input("Tanya Siti sesuatu..."):
    if user_input.strip():
        with st.chat_message("user"):
            st.write(user_input)
        
        if "chat_session_v2" in st.session_state:
            try:
                response = st.session_state.chat_session_v2.send_message(user_input)
                with st.chat_message("assistant"):
                    st.write(response.text)
            except Exception as e:
                st.error(f"Gagal memproses pesan: {e}")
                st.info("Silakan tunggu beberapa saat atau refresh halaman jika kuota Free Tier Anda terkena pembatasan rate limit harian.")
        else:
            st.error("Sesi obrolan gagal dimulai. Silakan restart aplikasi kamu.")
