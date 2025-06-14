import re
import fitz
from collections import Counter

def detect_inconsistencies(extracted_font_style, extracted_font_size, act_font_size, act_font_style, act_tolerance):
    font_lower = extracted_font_style.lower()

    font_matches = any(
        font_lower == _font_style.lower() for _font_style in act_font_style
    )

    size_matches = any(
        (act_size - act_tolerance) <= extracted_font_size <= (act_size + act_tolerance)
        for act_size in act_font_size
    )

    return font_matches and size_matches

def is_numeric(value):
    """Check if the text is a number like ₹5,00,000 or 1000.00"""
    value = value.replace('₹', '').replace(',', '').strip()
    return re.fullmatch(r'\d+(\.\d{1,2})?', value) is not None


def detect_font_outliers(user_fields, outlier_threshold=0.1):
    """Annotate fields with low-frequency font-size combinations"""
    all_fonts = [(f["font"], f["size"]) for f in user_fields]
    total = len(all_fonts)
    if total == 0:
        return

    font_counts = Counter(all_fonts)

    for field in user_fields:
        freq = font_counts.get((field["font"], field["size"]), 0) / total
        if freq < outlier_threshold:
            field.setdefault("meta", []).append({
                "reason": "font_outlier",
                "message": "Font and size combination used very rarely in this document.",
                "details": {
                    "observed_frequency": round(freq, 4),
                    "threshold": outlier_threshold
                }
            })
            field["is_outlier"] = True


def detect_position_outliers(user_fields, x_tolerance=15):
    """Mark user fields whose x0 position deviates from the median alignment"""
    numeric_fields = [f for f in user_fields if is_numeric(f["text"])]
    if not numeric_fields:
        return

    x0_list = [f["bbox"][0] for f in numeric_fields]
    sorted_x0 = sorted(x0_list)
    mid = len(sorted_x0) // 2
    median_x = sorted_x0[mid] if len(sorted_x0) % 2 else (sorted_x0[mid - 1] + sorted_x0[mid]) / 2

    for field in numeric_fields:
        x0 = field["bbox"][0]
        if abs(x0 - median_x) > x_tolerance:
            field.setdefault("meta", []).append({
                "reason": "position_outlier",
                "message": "X-position deviates from common alignment.",
                "details": {
                    "x0": round(x0, 2),
                    "expected_x0": round(median_x, 2),
                    "tolerance": x_tolerance
                }
            })
            field["is_outlier"] = True


def simulate_ocr_results(pdf_path, allowed_font_style, allowed_font_size, allowed_tolerance):
    """
    Utility function that parses a PDF and returns OCR fields as dictionaries.
    No model instances are created here.
    """
    doc = fitz.open(pdf_path)
    ocr_data = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    bbox = span["bbox"]
                    font = span["font"]
                    size = span["size"]

                    field_type = "template" if detect_inconsistencies(
                        font, size,
                        act_font_style=allowed_font_style,
                        act_font_size=allowed_font_size,
                        act_tolerance=allowed_tolerance
                    ) else "user"

                    ocr_data.append({
                        "page_number": page_num,
                        "bbox": bbox,
                        "font": font,
                        "size": size,
                        "text": text,
                        "field_type": field_type,
                        "meta": [],
                        "is_outlier": False
                    })

    return ocr_data
