import json
import os
import uuid
from datetime import datetime


# ==========================================
# DATA FILE
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "chats.json")


# ==========================================
# ENSURE DATA FILE
# ==========================================

def ensure_data_file():
    """
    Memastikan folder data dan chats.json tersedia.
    """

    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):

        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {},
                file,
                ensure_ascii=False,
                indent=2
            )


# ==========================================
# LOAD CHATS
# ==========================================

def load_chats():
    """
    Mengambil seluruh chat history dari JSON.
    """

    ensure_data_file()

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, dict):
                return data

            return {}

    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return {}


# ==========================================
# SAVE CHATS
# ==========================================

def save_chats(chats):
    """
    Menyimpan seluruh chat history ke JSON.
    """

    ensure_data_file()

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chats,
            file,
            ensure_ascii=False,
            indent=2
        )


# ==========================================
# CREATE CHAT
# ==========================================

def create_chat(title="Chat Baru"):
    """
    Membuat percakapan baru.
    """

    now = datetime.now().isoformat()

    chat_id = str(uuid.uuid4())

    return {
        "id": chat_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": []
    }


# ==========================================
# ADD CHAT
# ==========================================

def add_chat(chats, chat):
    """
    Menambahkan chat baru.
    """

    chats[chat["id"]] = chat

    save_chats(chats)


# ==========================================
# UPDATE CHAT
# ==========================================

def update_chat(chats, chat_id, messages):

    if chat_id not in chats:
        return

    chats[chat_id]["messages"] = messages

    chats[chat_id]["updated_at"] = (
        datetime.now().isoformat()
    )

    save_chats(chats)


# ==========================================
# DELETE CHAT
# ==========================================

def delete_chat(chats, chat_id):

    if chat_id not in chats:
        return False

    del chats[chat_id]

    save_chats(chats)

    return True


# ==========================================
# RENAME CHAT
# ==========================================

def rename_chat(chats, chat_id, title):

    if chat_id not in chats:
        return False

    chats[chat_id]["title"] = title

    chats[chat_id]["updated_at"] = (
        datetime.now().isoformat()
    )

    save_chats(chats)

    return True