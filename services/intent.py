INTENTS = {
    "greeting": "Sapaan atau percakapan pembuka.",
    
    "product_search": "Mencari produk berdasarkan kebutuhan, warna, ukuran, atau budget.",
    
    "product_price": "Menanyakan harga produk.",
    
    "product_stock": "Menanyakan ketersediaan produk, warna, atau ukuran.",
    
    "product_recommendation": "Meminta rekomendasi produk.",
    
    "order": "Menanyakan cara melakukan pemesanan.",
    
    "payment": "Menanyakan metode atau informasi pembayaran.",
    
    "shipping": "Menanyakan pengiriman, biaya, atau estimasi pengiriman.",
    
    "return": "Menanyakan retur atau penukaran barang.",
    
    "customer_service": "Meminta bantuan Customer Service.",
    
    "other": "Pertanyaan di luar layanan StyleUp.",
}

def detect_intent(user_input):
    """
    Mendeteksi intent berdasarkan keyword sederhana.
    """

    text = user_input.lower().strip()

    # ==========================================
    # GREETING
    # ==========================================

    greeting_words = [
        "halo",
        "hai",
        "hi",
        "hello",
        "pagi",
        "siang",
        "sore",
        "malam",
    ]

    if any (
        text == word or text.startswith(word + " ")
        for word in greeting_words
    ):
        return "greeting"

    # ==========================================
    # SHIPPING
    # ==========================================

    if any(word in text for word in [
        "ongkir",
        "pengiriman",
        "shipping",
        "dikirim",
        "kirim",
        "biaya kirim",
        "lama pengiriman",
        "estimasi pengiriman",
    ]):
        return "shipping"

    # ==========================================
    # PAYMENT
    # ==========================================

    if any(word in text for word in [
        "bayar",
        "pembayaran",
        "transfer",
        "cod",
        "metode pembayaran",
    ]):
        return "payment"

    # ==========================================
    # RETURN
    # ==========================================

    if any(word in text for word in [
        "retur",
        "return",
        "tukar",
        "ditukar",
        "penukaran",
    ]):
        return "return"

    # ==========================================
    # PRODUCT STOCK
    # ==========================================

    if any(word in text for word in [
        "stok",
        "stock",
        "tersedia",
        "ukuran",
        "size",
        "masih ada",
        "ada warna",
    ]):
        return "product_stock"

    # ==========================================
    # PRODUCT PRICE
    # ==========================================

    if any(word in text for word in [
        "harga",
        "harganya",
        "nominal",
        "bandrol",
        "berapa harga",
    ]):
        return "product_price"

    # ==========================================
    # PRODUCT RECOMMENDATION
    # ==========================================

    if any(word in text for word in [
        "rekomendasi",
        "sarankan",
        "saran",
        "cocok",
    ]):
        return "product_recommendation"

    # ==========================================
    # ORDER
    # ==========================================

    if any(word in text for word in [
        "pesan",
        "order",
        "pemesanan",
        "membeli",
        "beli",
        "cara pesan",
        "cara order",
    ]):
        return "order"

    # ==========================================
    # PRODUCT SEARCH
    # ==========================================

    if any(word in text for word in [
         "cari",
        "mencari",
        "carikan",
        "ada yang",
        "punya",
        "ada",
        "murah",
        "di bawah",
        "dibawah",
    ]):
        return "product_search"

    # ==========================================
    # CUSTOMER SERVICE
    # ==========================================

    if any(word in text for word in [
        "cs",
        "customer service",
        "admin",
        "bantuan",
        "hubungi",
    ]):
        return "customer_service"

    # ==========================================
    # OTHER
    # ==========================================

    return "other"