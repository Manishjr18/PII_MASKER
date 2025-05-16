import easyocr
import cv2
import re
from PIL import Image
import numpy as np
import os

reader = easyocr.Reader(['en', 'hi'])  # Multilingual OCR support

# Define all PII components and patterns
NAME_KEYWORDS = ["name", "नाम", "father", "mother", "guardian", "wife", "husband"]
ADDRESS_KEYWORDS = [
    "address", "पता", "village", "post", "po", "ps", "district", "city", "town",
    "state", "colony", "road", "lane", "near", "floor", "house", "maniyari", "area"
]
DOB_KEYWORDS = ["dob"]
ID_KEYWORDS = ["pan", "passport", "voter", "ration", "license", "driving", "epic"]

# Regex for patterns
REGEX_PATTERNS = [
    r'\d{4} \d{4} \d{4}',                   # Aadhaar format
    r'\b\d{10}\b',                          # Phone number
    r'\S+@\S+\.\S+',                        # Email
    r'\b\d{1,2}/\d{1,2}/\d{4}\b',           # DOB
    r'^[A-Z]{5}[0-9]{4}[A-Z]$',             # PAN card format
    r'[A-Z]{1,2}[0-9]{6,9}'                 # Passport, Driving license (generic)
]

def is_match(text, keywords):
    return any(k in text.lower() for k in keywords)

def matches_regex(text):
    return any(re.search(p, text) for p in REGEX_PATTERNS)

def process_image(image_path):
    image = cv2.imread(image_path)
    results = reader.readtext(image_path)

    mask_regions = []
    custom_boxes = []

    for i, (bbox, text, _) in enumerate(results):
        text_lower = text.lower()

        # ✅ Address - Large custom box
        if is_match(text, ADDRESS_KEYWORDS):
            center_x = int((bbox[0][0] + bbox[2][0]) / 2)
            center_y = int((bbox[0][1] + bbox[2][1]) / 2)
            width = 180  # wider box
            height = 160  # taller box
            top_left = (max(center_x - width // 2, 0), max(center_y - height // 2, 0))
            bottom_right = (center_x + width // 2, center_y + height // 2)
            custom_boxes.append((top_left, bottom_right))
            print(f"🏠 Address box: {text}")

        # ✅ DOB - mask DOB + name above
        elif is_match(text, DOB_KEYWORDS) or re.search(r'\b\d{1,2}/\d{1,2}/\d{4}\b', text):
            x1 = int(bbox[0][0])
            y1 = int(bbox[0][1] - 60)  # Go 100px above DOB
            x2 = int(bbox[2][0])
            y2 = int(bbox[2][1])
            top_left = (max(x1, 0), max(y1, 0))
            bottom_right = (x2, y2 + 10)
            custom_boxes.append((top_left, bottom_right))
            print(f"🎂 DOB box: {text}")

        # ✅ Name – mask this and next line
        elif is_match(text, NAME_KEYWORDS):
            mask_regions.append(bbox)
            if i + 1 < len(results):
                mask_regions.append(results[i + 1][0])
            print(f"👤 Name match: {text}")

        # ✅ PAN - label + number
        elif "pan" in text_lower:
            mask_regions.append(bbox)
            if i + 1 < len(results):
                mask_regions.append(results[i + 1][0])
            print(f"🪪 PAN match: {text}")

        # ✅ Regex patterns - Aadhaar, email, phone
        elif matches_regex(text):
            mask_regions.append(bbox)
            print(f"📌 Regex match: {text}")

        # ✅ Other ID keywords
        elif is_match(text, ID_KEYWORDS):
            mask_regions.append(bbox)
            print(f"🆔 ID keyword: {text}")

    # Draw standard black boxes
    for region in mask_regions:
        pts = np.array(region).astype(int)
        top_left = tuple(pts[0])
        bottom_right = tuple(pts[2])
        padding = 10
        cv2.rectangle(
            image,
            (top_left[0] - padding, top_left[1] - padding),
            (bottom_right[0] + padding, bottom_right[1] + padding),
            (0, 0, 0), -1
        )

    # Draw custom boxes
    for top_left, bottom_right in custom_boxes:
        cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), -1)

    # Convert and save
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)

    filename = os.path.basename(image_path)
    output_path = os.path.join("output", f"masked_{filename}")
    pil_image.save(output_path)

    print(f"✅ Final image saved at: {output_path}")
    return pil_image
