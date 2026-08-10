import streamlit as st
import streamlit.components.v1 as components

from services.openrouter import generate_response
from services.catalog import SYSTEM_PROMPT
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
    create_chat,
    add_chat,
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
    # USER MESSAGE
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
    # DETECT INTENT
    # ======================================
    intent = detect_intent(user_input)
    print(f"[INTENT] {intent}")
    # ======================================
    # PRODUCT SEARCH
    # ======================================

    product_context = ""

    if intent == "product_search":
        results = search_products(user_input)
        product_context = format_product_results(
            results
        )

        print(product_context)
    intent_instruction = get_intent_instruction(
        intent
    )
    

    # ======================================
    # GUARDRAIL
    # ======================================
    if not is_styleup_topic(user_input):
        with st.chat_message("assistant"):
            response = get_guardrail_message()
            st.markdown(response)

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

    intent_instruction = get_intent_instruction(
    intent
    )

    guardrail_context = build_guardrail_context(
        intent
    )

    print(
    f"[INTENT INSTRUCTION] "
    f"{intent_instruction}"
    )
    


    # ======================================
    # AUTO TITLE
    # ======================================

    if len(messages) == 2:

        current_chat["title"] = (
            user_input[:40]
        )


    # ======================================
    # GENERATE AI RESPONSE
    # ======================================

    try:

        with st.chat_message("assistant"):

            placeholder = st.empty()

            full_response = ""

              # ==================================
            # BUAT CONTEXT KHUSUS UNTUK AI
            # ==================================

            ai_messages = messages.copy()
            ai_messages.append(
                {
                    "role":"system",
                    "content": (
                        "INSTRUKSI INTENT INTERNAL:\n"
                        + intent_instruction
                        + "\n\n"
                        + guardrail_context
                        + "\n\n"
                        + product_context
                    ),
                }
            )

            stream = generate_response(
                ai_messages
            )

            # ==============================
            # STREAMING
            # ==============================

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
                        full_response + "▌"
                    )

            placeholder.markdown(
                full_response
            )


            # ==============================
            # COPY BUTTON
            # ==============================

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
        # ASSISTANT MESSAGE
        # ==================================

        messages.append(
            {
                "role": "assistant",
                "content": full_response,
            }
        )


        # ==================================
        # SAVE CHAT
        # ==================================

        update_chat(
            st.session_state.chats,
            st.session_state.current_chat_id,
            messages,
        )


    except Exception as e:

        st.error(
            f"Gagal memproses pesan via OpenRouter: {e}"
        )

        st.info(
            "Pastikan kuota akun OpenRouter "
            "Anda mencukupi atau model sedang "
            "tidak sibuk."
        )