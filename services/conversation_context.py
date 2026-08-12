# ==========================================
# CONTEXT SERVICE
# ==========================================

def get_recent_messages(messages, limit=6):
    """
    Mengambil beberapa pesan terakhir
    untuk digunakan sebagai konteks.
    """

    if not messages:
        return []

    return messages[-limit:]


def build_conversation_context(messages):
    """
    Membuat context percakapan dalam bentuk teks.
    """

    recent_messages = get_recent_messages(
        messages,
        limit=6
    )

    if not recent_messages:
        return ""

    context_lines = []

    for message in recent_messages:

        role = message.get("role")
        content = message.get("content", "")

        # Jangan masukkan system prompt
        if role == "system":
            continue

        if role == "user":
            context_lines.append(
                f"Pelanggan: {content}"
            )

        elif role == "assistant":
            context_lines.append(
                f"Siti: {content}"
            )

    return "\n".join(context_lines)

def needs_context(user_input):
    """
    Mengecek apakah pertanyaan kemungkinan
    bergantung pada percakapan sebelumnya.
    """

    text = user_input.lower().strip()

    context_keywords = [
        "yang tadi",
        "tadi",
        "itu",
        "tersebut",
        "yang itu",
        "yang tadi kamu bilang",
        "kalau yang",
        "kalau",
        "bagaimana dengan",
        "gimana dengan",
        "yang lain",
        "lainnya",
        "berapa",
        "ukuran",
        "size",
        "warna",
        "harganya",
        "kalau putih",
        "kalau hitam",
        "kalau merah",
        "kalau biru",
    ]

    return any(
        keyword in text
        for keyword in context_keywords
    )