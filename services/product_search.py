import re

from services.catalog import PRODUCTS


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):
    """
    Menormalisasi teks pelanggan agar pencarian lebih fleksibel.
    """

    text = text.lower().strip()

    replacements = {
        "rb": "ribu",
        "k": "ribu",
        "murmer": "murah",
        "terjangkau": "murah",
        "hemat": "murah",
        "budget rendah": "murah",
        "dibawah": "bawah",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


# =========================================================
# EXTRACT BUDGET
# =========================================================

def extract_budget(text):
    """
    Mengambil batas harga dari pertanyaan pelanggan.

    Contoh:
        100 ribu
        100rb
        100k
        100000
    """

    text = text.lower().strip()

    # -----------------------------------------
    # Format: 100 ribu
    # -----------------------------------------

    match = re.search(
        r"(\d+(?:[.,]\d+)?)\s*ribu",
        text,
    )

    if match:

        number = float(
            match.group(1).replace(",", ".")
        )

        return int(number * 1000)

    # -----------------------------------------
    # Format: 100000
    # -----------------------------------------

    match = re.search(
        r"\b(\d{4,7})\b",
        text,
    )

    if match:

        return int(match.group(1))

    return None


# =========================================================
# DETECT PRICE PREFERENCE
# =========================================================

def detect_price_preference(text):
    """
    Menentukan apakah pelanggan mencari
    produk murah atau memiliki batas harga.
    """

    text = normalize_text(text)

    cheap_keywords = [
        "murah",
        "hemat",
        "harga rendah",
    ]

    for keyword in cheap_keywords:

        if keyword in text:
            return "cheap"

    if any(
        keyword in text
        for keyword in [
            "bawah",
            "maksimal",
            "sampai",
            "budget",
        ]
    ):

        return "maximum"

    return None


# =========================================================
# DETECT COLOR
# =========================================================

def detect_colors(text):
    """
    Mendeteksi warna dari pertanyaan pelanggan.
    """

    text = normalize_text(text)

    detected_colors = []

    color_aliases = {

        "hitam": [
            "hitam",
            "gelap",
        ],

        "putih": [
            "putih",
        ],

        "merah": [
            "merah",
        ],

        "biru": [
            "biru",
            "navy",
        ],

        "hijau": [
            "hijau",
            "sage green",
        ],

        "ungu": [
            "ungu",
            "lilac",
        ],

        "krem": [
            "krem",
        ],

        "abu-abu": [
            "abu-abu",
            "abu abu",
            "abu",
        ],
    }

    for color, aliases in color_aliases.items():

        for alias in aliases:

            if alias in text:

                detected_colors.append(color)

                break

    return detected_colors


# =========================================================
# PRODUCT COLOR MATCH
# =========================================================

def product_matches_color(product, colors):
    """
    Mengecek apakah produk memiliki warna
    yang diminta pelanggan.
    """

    if not colors:
        return True

    product_colors = [
        color.lower()
        for color in product["colors"]
    ]

    for requested_color in colors:

        # HITAM
        if requested_color == "hitam":

            if any(
                "hitam" in color
                for color in product_colors
            ):
                return True

        # PUTIH
        elif requested_color == "putih":

            if any(
                "putih" in color
                for color in product_colors
            ):
                return True

        # MERAH
        elif requested_color == "merah":

            if any(
                "merah" in color
                for color in product_colors
            ):
                return True

        # BIRU / NAVY
        elif requested_color == "biru":

            if any(
                "biru" in color
                or "navy" in color
                for color in product_colors
            ):
                return True

        # HIJAU / SAGE
        elif requested_color == "hijau":

            if any(
                "hijau" in color
                or "sage" in color
                for color in product_colors
            ):
                return True

        # UNGU / LILAC
        elif requested_color == "ungu":

            if any(
                "ungu" in color
                or "lilac" in color
                for color in product_colors
            ):
                return True

        # KREM
        elif requested_color == "krem":

            if any(
                "krem" in color
                for color in product_colors
            ):
                return True

        # ABU-ABU
        elif requested_color == "abu-abu":

            if any(
                "abu" in color
                for color in product_colors
            ):
                return True

    return False


# =========================================================
# PRODUCT SEARCH
# =========================================================

def search_products(user_input):
    """
    Mencari produk berdasarkan:

    - Nama produk
    - Warna
    - Budget
    - Preferensi murah
    """

    original_text = user_input.lower().strip()

    text = normalize_text(
        original_text
    )

    budget = extract_budget(
        original_text
    )

    price_preference = detect_price_preference(
        text
    )

    colors = detect_colors(
        text
    )

    results = []

    # =====================================================
    # LOOP PRODUCT
    # =====================================================

    for product in PRODUCTS:

        score = 0

        product_name = product[
            "name"
        ].lower()

        # =================================================
        # 1. FILTER BUDGET
        # =================================================

        if budget is not None:

            if product["price"] > budget:

                continue

            score += 5

        # =================================================
        # 2. FILTER WARNA
        # =================================================

        if colors:

            if not product_matches_color(
                product,
                colors,
            ):

                continue

            score += 5

        # =================================================
        # 3. PRODUCT NAME
        # =================================================

        product_words = product_name.split()

        for word in product_words:

            if word in text:

                score += 2

        # =================================================
        # 4. CHEAP
        # =================================================

        if price_preference == "cheap":

            # Produk di bawah / sama dengan 100 ribu
            if product["price"] <= 100000:

                score += 3

        # =================================================
        # 5. MAXIMUM WITHOUT EXPLICIT NUMBER
        # =================================================

        if (
            price_preference == "maximum"
            and budget is None
        ):

            score += 1

        # =================================================
        # 6. HASIL
        # =================================================

        # Jika user memberikan filter tertentu,
        # produk harus memenuhi filter tersebut.

        if score > 0:

            results.append(
                {
                    "product": product,
                    "score": score,
                }
            )

    # =====================================================
    # SORT
    # =====================================================

    results.sort(
        key=lambda item: (
            -item["score"],
            item["product"]["price"],
        )
    )

    return results


# =========================================================
# FORMAT RESULT
# =========================================================

def format_product_results(results):
    """
    Mengubah hasil pencarian menjadi teks
    yang dapat diberikan ke AI.
    """

    if not results:

        return (
            "Tidak ditemukan produk yang "
            "sesuai dengan kriteria pelanggan."
        )

    lines = [
        "HASIL PENCARIAN PRODUK STYLEUP:"
    ]

    for item in results:

        product = item["product"]

        lines.append(
            f"""
- {product["name"]}
  Warna: {", ".join(product["colors"])}
  Ukuran: {", ".join(product["sizes"])}
  Harga: Rp{product["price"]:,}
""".strip()
        )

    return "\n".join(lines)