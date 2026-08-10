from services.catalog import PRODUCT_CATALOG, FAQ


# ==========================================
# TOPIC KEYWORDS
# ==========================================

ALLOWED_KEYWORDS = [
    # Produk
    "baju",
    "kaos",
    "kemeja",
    "celana",
    "flanel",
    "chino",
    "produk",
    "harga",
    "stok",
    "ukuran",
    "warna",

    # Belanja
    "beli",
    "pesan",
    "order",
    "pemesanan",
    "belanja",

    # Customer Service
    "pembayaran",
    "bayar",
    "cod",
    "pengiriman",
    "ongkir",
    "kirim",
    "retur",
    "return",
    "tukar",
    "penukaran",
    "cs",
    "customer service",

    # Fashion
    "fashion",
    "pakaian",
    "outfit",
    "style",
    "gaya",
]


def is_styleup_topic(user_input):
    """
    Mengecek apakah pertanyaan masih berkaitan
    dengan StyleUp, fashion, produk, atau layanan CS.
    """

    text = user_input.lower().strip()

    return any(
        keyword in text
        for keyword in ALLOWED_KEYWORDS
    )


def get_guardrail_message():
    """
    Pesan ketika pertanyaan berada di luar
    konteks StyleUp.
    """

    return (
        "Maaf ya, Kak 😊 "
        "Siti hanya dapat membantu mengenai produk, "
        "fashion, belanja, dan layanan Customer Service "
        "StyleUp. 🛍️✨"
    )


def build_guardrail_context(intent):
    """
    Membuat instruksi keamanan untuk AI.
    """

    return f"""
GUARDRAIL CUSTOMER SERVICE STYLEUP

Intent pelanggan:
{intent}

ATURAN WAJIB:

1. Jangan mengarang informasi produk.
2. Jangan mengarang harga.
3. Jangan mengarang warna.
4. Jangan mengarang ukuran.
5. Jangan mengarang stok aktual.
6. Jangan mengarang metode pembayaran.
7. Jangan mengarang biaya pengiriman.
8. Jangan mengarang kebijakan retur.
9. Gunakan hanya informasi dari katalog produk dan FAQ StyleUp.
10. Jika informasi tidak tersedia, katakan bahwa informasi tersebut
    belum tersedia.
11. Jika pertanyaan berada di luar konteks StyleUp,
    arahkan pelanggan kembali ke layanan StyleUp.
12. Jangan mengklaim memiliki informasi yang tidak terdapat
    dalam katalog atau FAQ.
"""