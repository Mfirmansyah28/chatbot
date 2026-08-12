import streamlit as st
import streamlit.components.v1 as components

from services.openrouter import generate_response

from services.intent import detect_intent

from services.intent_context import (
    get_intent_instruction
)

from services.conversation_context import (
    build_conversation_context,
    needs_context
)

from services.guardrail import (
    is_styleup_topic,
    get_guardrail_message,
    build_guardrail_context
)

from services.product_search import (
    search_products,
    format_product_results
)

from services.chat_manager import (
    load_chats,
    update_chat
)

from ui.sidebar import render_sidebar


# ==========================================
# 1. SETUP HALAMAN
# ==========================================

st.set_page_config(
    page_title="StyleUp Chatbot CS",
    page_icon="🛍️",
)


# ==========================================
# 2. CEK API KEY
# ==========================================

try:

    API_KEY = st.secrets[
        "OPENROUTER_API_KEY"
    ]

except KeyError:

    st.error(
        "Error: API Key "
        "'OPENROUTER_API_KEY' "
        "tidak ditemukan di "
        ".streamlit/secrets.toml"
    )

    st.stop()


# ==========================================
# 3. INITIALIZE CHAT HISTORY
# ==========================================

if "chats" not in st.session_state:

    st.session_state.chats = load_chats()


# ==========================================
# 4. INITIALIZE CURRENT CHAT
# ==========================================

if "current_chat_id" not in st.session_state:

    st.session_state.current_chat_id = None


# ==========================================
# 5. SIDEBAR
# ==========================================

render_sidebar()


# ==========================================
# 6. CURRENT CHAT
# ==========================================

current_chat_id = (
    st.session_state.current_chat_id
)


if (
    current_chat_id is not None
    and current_chat_id
    in st.session_state.chats
):

    current_chat = (
        st.session_state.chats[
            current_chat_id
        ]
    )

    messages = current_chat[
        "messages"
    ]

else:

    current_chat = None

    messages = []


# ==========================================
# 7. HEADER
# ==========================================

st.title(
    "🛍️ StyleUp - AI Customer Service"
)

st.write(
    "Halo! Selamat datang di StyleUp. "
    "Ada yang bisa Siti bantu hari ini? 😊"
)


# ==========================================
# 8. TAMPILKAN RIWAYAT PESAN
# ==========================================

for message in messages:

    # Jangan tampilkan system message
    if message["role"] == "system":
        continue

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==========================================
# 9. CHAT INPUT
# ==========================================

if user_input := st.chat_input(
    "Tanya Siti sesuatu..."
):

    # ======================================
    # VALIDASI INPUT
    # ======================================

    if not user_input.strip():

        st.stop()


    # ======================================
    # PASTIKAN CHAT AKTIF
    # ======================================

    if current_chat is None:

        st.warning(
            "Silakan klik ➕ New Chat "
            "terlebih dahulu."
        )

        st.stop()


    # ======================================
    # TAMPILKAN USER MESSAGE
    # ======================================

    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # ======================================
    # SIMPAN USER MESSAGE
    # ======================================

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )


    # ======================================
    # AUTO TITLE
    # ======================================

    if len(messages) == 2:

        current_chat["title"] = (
            user_input[:40]
        )


    # ======================================
    # 10. DETECT INTENT
    # ======================================

    intent = detect_intent(
        user_input
    )

    print(
        f"[INTENT] {intent}"
    )


    # ======================================
    # 11. CONVERSATION CONTEXT
    # ======================================

    conversation_context = ""


    if needs_context(
        user_input
    ):

        conversation_context = (
            build_conversation_context(
                messages
            )
        )

        print(
            "[CONTEXT] "
            "Menggunakan konteks percakapan"
        )

        print(
            conversation_context
        )


    # ======================================
    # 12. GUARDRAIL
    # ======================================

    if not is_styleup_topic(
        user_input
    ):

        with st.chat_message(
            "assistant"
        ):

            response = (
                get_guardrail_message()
            )

            st.markdown(
                response
            )


        messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )


        update_chat(
            st.session_state.chats,
            st.session_state.current_chat_id,
            messages,
        )


        st.stop()


    # ======================================
    # 13. INTENT INSTRUCTION
    # ======================================

    intent_instruction = (
        get_intent_instruction(
            intent
        )
    )


    print(
        "[INTENT INSTRUCTION]"
    )

    print(
        intent_instruction
    )


    # ======================================
    # 14. GUARDRAIL CONTEXT
    # ======================================

    guardrail_context = (
        build_guardrail_context(
            intent
        )
    )


    # ======================================
    # 15. PRODUCT SEARCH
    # ======================================

    product_context = ""


    if intent == "product_search":

        results = search_products(
            user_input
        )


        print(
            "[PRODUCT SEARCH]"
        )


        print(
            [
                (
                    result["product"]["name"],
                    result["product"]["price"]
                )
                for result in results
            ]
        )


        product_context = (
            format_product_results(
                results
            )
        )


        print(
            "[PRODUCT CONTEXT]"
        )

        print(
            product_context
        )


    # ======================================
    # 16. INTERNAL CONTEXT
    # ======================================

    internal_context = f"""
INSTRUKSI INTENT INTERNAL:

{intent_instruction}


GUARDRAIL CUSTOMER SERVICE:

{guardrail_context}
"""


    # ======================================
    # 17. CONVERSATION CONTEXT
    # ======================================

    if conversation_context:

        internal_context += f"""

KONTEKS PERCAKAPAN SEBELUMNYA:

{conversation_context}


ATURAN CONVERSATION CONTEXT:

1. Gunakan konteks percakapan sebelumnya
   jika masih relevan dengan pertanyaan
   pelanggan.

2. Pahami pertanyaan lanjutan seperti:
   - "Berapa harganya?"
   - "Ada warna lain?"
   - "Kalau yang putih?"
   - "Yang tadi berapa?"
   - "Ada ukuran L?"
   - "Saya mau yang itu."

3. Hubungkan kata seperti:
   "itu", "yang tadi", "produk tersebut",
   "yang hitam", "yang putih", dan
   "yang itu" dengan pembahasan sebelumnya
   jika konteksnya jelas.

4. Jangan meminta pelanggan mengulangi
   informasi yang sudah jelas dari
   percakapan sebelumnya.

5. Jangan menggunakan konteks jika tidak
   berhubungan dengan pertanyaan saat ini.

6. Jangan mengarang informasi baru dari
   konteks percakapan.

7. Informasi harga, warna, ukuran, dan
   produk tetap harus mengikuti katalog
   StyleUp.

8. Jika informasi yang dibutuhkan tidak
   tersedia, katakan dengan jujur bahwa
   informasi tersebut belum tersedia.
"""


    # ======================================
    # 18. PRODUCT CONTEXT
    # ======================================

    if product_context:

        internal_context += f"""

HASIL PENCARIAN PRODUK STYLEUP:

{product_context}


ATURAN PRODUCT SEARCH:

1. Gunakan hasil pencarian di atas sebagai
   sumber informasi produk.

2. Jangan mengarang produk.

3. Jangan mengarang harga.

4. Jangan mengarang warna.

5. Jangan mengarang ukuran.

6. Jangan mengarang stok.

7. Jangan memberikan produk yang tidak
   terdapat dalam hasil pencarian.

8. Jika hasil pencarian mengatakan produk
   tidak ditemukan, sampaikan bahwa produk
   yang sesuai belum tersedia.

9. Jawab secara singkat dan natural
   sebagai Siti.
"""


    # ======================================
    # 19. DEBUG INTERNAL CONTEXT
    # ======================================

    print(
        "\n========== INTERNAL CONTEXT =========="
    )

    print(
        internal_context
    )

    print(
        "======================================\n"
    )


    # ======================================
    # 20. BUAT MESSAGE UNTUK AI
    # ======================================

    messages_for_ai = list(
        messages
    )


    messages_for_ai.append(
        {
            "role": "system",
            "content": internal_context,
        }
    )


    # ======================================
    # 21. GENERATE AI RESPONSE
    # ======================================

    try:

        with st.chat_message(
            "assistant"
        ):

            placeholder = st.empty()

            full_response = ""


            # ==================================
            # OPENROUTER STREAMING
            # ==================================

            stream = generate_response(
                messages_for_ai
            )


            # ==================================
            # STREAM RESPONSE
            # ==================================

            for chunk in stream:

                if (
                    chunk.choices
                    and chunk.choices[0].delta
                    and chunk.choices[0]
                    .delta.content
                ):

                    token = (
                        chunk.choices[0]
                        .delta
                        .content
                    )


                    full_response += (
                        token
                    )


                    placeholder.markdown(
                        full_response
                        + "▌"
                    )


            # ==================================
            # FINAL RESPONSE
            # ==================================

            placeholder.markdown(
                full_response
            )


            # ==================================
            # COPY RESPONSE
            # ==================================

            if st.button(
                "📋 Copy Response",
                key=(
                    f"copy_"
                    f"{len(messages)}"
                ),
            ):

                components.html(
                    f"""
                    <script>
                    navigator.clipboard.writeText(
                        `{full_response}`
                    );
                    </script>
                    """,
                    height=0,
                )


                st.toast(
                    "Jawaban berhasil "
                    "disalin 😊"
                )


        # ==================================
        # 22. SIMPAN ASSISTANT MESSAGE
        # ==================================

        messages.append(
            {
                "role": "assistant",
                "content": full_response,
            }
        )


        # ==================================
        # 23. SAVE CHAT
        # ==================================

        update_chat(
            st.session_state.chats,
            st.session_state.current_chat_id,
            messages,
        )


    # ======================================
    # 24. ERROR HANDLING
    # ======================================

    except Exception as e:

        st.error(
            "Gagal memproses pesan via "
            f"OpenRouter: {e}"
        )


        st.info(
            "Pastikan kuota akun OpenRouter "
            "Anda mencukupi atau model sedang "
            "tidak sibuk."
        )