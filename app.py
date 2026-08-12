import streamlit as st
import streamlit.components.v1 as components

from services.openrouter import generate_response
from services.intent import detect_intent
from services.intent_context import get_intent_instruction

from services.guardrail import (
    is_styleup_topic,
    get_guardrail_message,
    build_guardrail_context,
)

from services.product_search import (
    search_products,
    format_product_results,
)

from services.chat_manager import (
    load_chats,
    update_chat,
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

    API_KEY = st.secrets["OPENROUTER_API_KEY"]

except KeyError:

    st.error(
        "Error: API Key 'OPENROUTER_API_KEY' "
        "tidak ditemukan di .streamlit/secrets.toml"
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
    and current_chat_id in st.session_state.chats
):

    current_chat = (
        st.session_state.chats[
            current_chat_id
        ]
    )

    messages = current_chat["messages"]

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
            "Silakan klik ➕ New Chat terlebih dahulu."
        )

        st.stop()


    # ======================================
    # TAMPILKAN USER MESSAGE
    # ======================================

    with st.chat_message("user"):

        st.markdown(user_input)


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
    # DETECT INTENT
    # ======================================

    intent = detect_intent(
        user_input
    )

    print(
        f"[INTENT] {intent}"
    )


    # ======================================
    # GUARDRAIL
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
    # INTENT INSTRUCTION
    # ======================================

    intent_instruction = (
        get_intent_instruction(
            intent
        )
    )

    print(
        f"[INTENT INSTRUCTION] "
        f"{intent_instruction}"
    )


    # ======================================
    # GUARDRAIL CONTEXT
    # ======================================

    guardrail_context = (
        build_guardrail_context(
            intent
        )
    )


    # ======================================
    # PRODUCT SEARCH
    # ======================================

    product_context = ""


    if intent == "product_search":

        results = search_products(
            user_input
        )


        print(
            "[PRODUCT SEARCH]",
            [
                (
                    r["product"]["name"],
                    r["product"]["price"]
                )
                for r in results
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
    # BUAT CONTEXT INTERNAL UNTUK AI
    # ======================================

    internal_context = f"""
INSTRUKSI INTENT INTERNAL:

{intent_instruction}


GUARDRAIL CONTEXT:

{guardrail_context}
"""


    # ======================================
    # TAMBAHKAN PRODUCT CONTEXT
    # ======================================

    if product_context:

        internal_context += f"""

HASIL PENCARIAN PRODUK STYLEUP:

{product_context}


ATURAN PRODUCT SEARCH:

- Gunakan hasil pencarian di atas sebagai sumber
  informasi produk.
- Jangan mengarang produk.
- Jangan mengarang harga.
- Jangan mengarang warna.
- Jangan mengarang ukuran.
- Jangan memberikan produk yang tidak terdapat
  dalam hasil pencarian.
- Jika hasil pencarian mengatakan produk tidak
  ditemukan, sampaikan bahwa produk yang sesuai
  belum tersedia.
- Jawab secara singkat dan natural sebagai Siti.
"""


    # ======================================
    # BUAT MESSAGE UNTUK AI
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
    # GENERATE AI RESPONSE
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


            for chunk in stream:

                if (
                    chunk.choices
                    and chunk.choices[0].delta
                    and chunk.choices[0].delta.content
                ):

                    token = (
                        chunk.choices[0]
                        .delta
                        .content
                    )


                    full_response += token


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
            # COPY BUTTON
            # ==================================

            if st.button(
                "📋 Copy Response",
                key=f"copy_{len(messages)}",
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
                    "Jawaban berhasil disalin 😊"
                )


        # ==================================
        # SIMPAN ASSISTANT MESSAGE
        # ==================================

        messages.append(
            {
                "role": "assistant",
                "content": full_response,
            }
        )


        # ==================================
        # SIMPAN CHAT
        # ==================================

        update_chat(
            st.session_state.chats,
            st.session_state.current_chat_id,
            messages,
        )


    # ======================================
    # ERROR HANDLING
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