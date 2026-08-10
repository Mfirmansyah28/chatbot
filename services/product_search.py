import re

from services.catalog import PRODUCTS


def extract_budget(text):
    """
    Mengambil batas harga dari pertanyaan user.

    Contoh:
    "di bawah 100 ribu"
    → 100000
    """

    text = text.lower()

    # Contoh: 100 ribu
    match = re.search(
        r"(\d+(?:[.,]\d+)?)\s*(ribu|rb)",
        text,
    )

    if match:

        number = float(
            match.group(1).replace(",", ".")
        )

        return int(number * 1000)

    # Contoh: 100000
    match = re.search(
        r"\b(\d{4,7})\b",
        text,
    )

    if match:

        return int(match.group(1))

    return None


def search_products(user_input):
    """
    Mencari produk berdasarkan query user.
    """

    text = user_input.lower()

    budget = extract_budget(text)

    results = []

    for product in PRODUCTS:

        score = 0

        product_name = product["name"].lower()

        # ======================================
        # PRODUCT NAME
        # ======================================

        if any(
            word in product_name
            for word in text.split()
        ):
            score += 1

        # ======================================
        # COLOR
        # ======================================

        for color in product["colors"]:

            if color.lower() in text:

                score += 3

        # ======================================
        # PRICE
        # ======================================

        if budget is not None:

            if product["price"] <= budget:

                score += 5

            else:

                continue

        # ======================================
        # RESULT
        # ======================================

        if score > 0:

            results.append(
                {
                    "product": product,
                    "score": score,
                }
            )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results

def format_product_results(results):
    """
    Mengubah hasil pencarian menjadi context
    yang dapat dibaca oleh AI.
    """

    if not results:

        return (
            "Tidak ditemukan produk yang sesuai "
            "dengan kriteria pelanggan."
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
"""
        )

    return "\n".join(lines)