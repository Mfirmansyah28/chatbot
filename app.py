import streamlit as st
from openai import OpenAI

# 1. Mengambil API Key OpenRouter secara aman dari secrets.toml
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except KeyError:
    st.error("Error: API Key 'OPENROUTER_API_KEY' tidak ditemukan di .streamlit/secrets.toml")
    st.stop()

# 2. Masukkan System Instructions & Katalog Toko
system_instruction = """
Kamu adalah "Siti", Customer Service resmi dari toko fashion StyleUp.

Kepribadian:
- Ramah
- Profesional
- Sopan
- Singkat
- Informatif

Selalu berbicara menggunakan Bahasa Indonesia yang natural seperti Customer Service profesional di Indonesia.

Jangan pernah menggunakan kata yang tidak memiliki arti seperti:
"kabar saskah", "etuh", atau kata acak lainnya.

Gunakan kalimat yang rapi dan mudah dipahami.

Aturan yang WAJIB kamu patuhi:
1. Gunakan Bahasa Indonesia yang ramah dan kasual, gunakan panggilan "Kak" atau "Kakak" kepada pelanggan.
2. Selalu gunakan emoji yang relevan agar terkesan ramah (seperti 😊,🛍️,✨).
3. Jika pelanggan bertanya hal di luar topik toko fashion, belanja, atau gaya berpakaian, tolak dengan halus dan ingatkan kembali tugasmu sebagai CS StyleUp.
4. JAWABLAH PERTANYAAN STOK DAN HARGA HANYA BERDASARKAN DATA DI BAWAH INI. Jika tidak ada di data, katakan stok sedang kosong atau belum tersedia.
5. Gunakan Bahasa Indonesia yang baku, alami, dan mudah dipahami.
6. Jangan pernah membuat kata yang tidak ada dalam Bahasa Indonesia.
7. Jangan menggunakan typo, kata acak, kata tidak jelas, atau bahasa yang tidak bermakna.
8. Jika informasi tidak tersedia, jawab dengan sopan tanpa mengarang.
9. Berikan jawaban singkat, jelas, dan profesional.
10. Jangan mengulang kalimat yang sama.
11. Jangan mencampur bahasa Indonesia dengan bahasa lain kecuali diminta pengguna.

=== DATA KATALOG PRODUK STYLEUP ===
1. Kemeja Flanel Kotak-Kotak (Merah-Hitam, Biru-Navy) | M, L, XL | Rp 150.000
2. Kaos Polos Katun Premium (Hitam, Putih, Sage Green, Lilac) | S, M, L, XL | Rp 75.000
3. Celana Chino Slimfit (Krem, Hitam, Abu-abu) | 28, 30, 32, 34 | Rp 200.000
"""

# 3. Setup Halaman Tampilan Web Streamlit
st.set_page_config(page_title="StyleUp Chatbot CS", page_icon="🛍️")
st.title("🛍️ StyleUp - AI Customer Service")
st.write("Halo! Selamat datang di StyleUp. Ada yang bisa Siti bantu hari ini?")

# 4. Inisialisasi Client OpenRouter (Menggunakan SDK OpenAI)
if "client" not in st.session_state:
    st.session_state.client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY
    )

# 5. Inisialisasi Riwayat Obrolan Mandiri
if "messages" not in st.session_state:
    # Memasukkan system instruction di awal sebagai memori dasar AI
    st.session_state.messages = [
        {"role": "system", "content": system_instruction}
    ]

# 6. Tampilkan Riwayat Obrolan di Layar (Kecuali instruksi sistem)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# 7. Kotak Input Chat
if user_input := st.chat_input("Tanya Siti sesuatu..."):
    if user_input.strip():
        # Tampilkan chat kiriman user di layar
        with st.chat_message("user"):
            st.write(user_input)
        
        # Simpan pesan user ke dalam riwayat session_state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Kirim seluruh riwayat ke OpenRouter
try:

    with st.chat_message("assistant"):

        placeholder = st.empty()
        full_response = ""

        stream = st.session_state.client.chat.completions.create(
            model="nvidia/nemotron-3-nano-30b-a3b:free",
            messages=st.session_state.messages,
            stream=True,
        )

        for chunk in stream:

            if (
                chunk.choices
                and chunk.choices[0].delta
                and chunk.choices[0].delta.content
            ):
                token = chunk.choices[0].delta.content
                full_response += token
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
        }
    )

except Exception as e:
    st.error(f"Gagal memproses pesan via OpenRouter: {e}")
    st.info("Pastikan kuota akun OpenRouter Anda mencukupi atau model sedang tidak sibuk.")