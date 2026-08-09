import streamlit as st

from services.chat_manager import (
    create_chat,
    add_chat,
    delete_chat,
)

from services.catalog import SYSTEM_PROMPT


# ==========================================
# CREATE NEW CHAT
# ==========================================

def create_new_chat():

    new_chat = create_chat("Chat Baru")

    new_chat["messages"] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    add_chat(
        st.session_state.chats,
        new_chat,
    )

    st.session_state.current_chat_id = new_chat["id"]


# ==========================================
# SIDEBAR
# ==========================================

def render_sidebar():

    with st.sidebar:

        # ==================================
        # HEADER
        # ==================================

        st.title("🛍️ StyleUp")

        st.caption(
            "AI Customer Service"
        )

        # ==================================
        # NEW CHAT
        # ==================================

        if st.button(
            "➕ New Chat",
            use_container_width=True,
            key="new_chat_button",
        ):

            create_new_chat()

            st.rerun()

        st.divider()

        # ==================================
        # CHAT HISTORY
        # ==================================

        st.subheader(
            "💬 Riwayat Chat"
        )

        chats = st.session_state.chats

        # ==================================
        # EMPTY STATE
        # ==================================

        if not chats:

            st.caption(
                "Belum ada riwayat chat."
            )

            return

        # ==================================
        # CHAT LIST
        # ==================================

        for chat_id, chat in list(
            chats.items()
        ):

            col1, col2 = st.columns(
                [5, 1]
            )

            # ==============================
            # CHAT BUTTON
            # ==============================

            with col1:

                if st.button(
                    f"💬 {chat['title']}",
                    key=f"chat_{chat_id}",
                    use_container_width=True,
                ):

                    st.session_state.current_chat_id = (
                        chat_id
                    )

                    st.rerun()

            # ==============================
            # DELETE BUTTON
            # ==============================

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{chat_id}",
                ):

                    delete_chat(
                        st.session_state.chats,
                        chat_id,
                    )

                    # ==========================
                    # Jika chat aktif dihapus
                    # ==========================

                    if (
                        st.session_state.current_chat_id
                        == chat_id
                    ):

                        remaining_chats = (
                            st.session_state.chats
                        )

                        if remaining_chats:

                            # Jangan otomatis membuka
                            # chat lama.
                            st.session_state.current_chat_id = None

                        else:

                            # Tidak ada chat lagi
                            st.session_state.current_chat_id = None

                    st.rerun()