import joblib
import pandas as pd
import re
from fastapi import FastAPI, UploadFile, File
from PIL import Image
import pytesseract
import io

app = FastAPI()

# --- Load the trained model once ---
clf = joblib.load('line_classifier.pkl')

# --- Feature extraction function (must match training) ---
def extract_features(line):
    line = str(line)
    return {
        'length': len(line),
        'num_digits': sum(c.isdigit() for c in line),
        'num_alpha': sum(c.isalpha() for c in line),
        'has_unit': int(bool(re.search(r'(g/dL|%|mg/L|mmol/L)', line))),
        'has_decimal': int(bool(re.search(r'\d+\.\d+', line))),
        'has_range': int('-' in line),
        'is_upper': int(line.isupper()),
        'has_colon': int(':' in line),
        'is_digit_line': int(line.replace('.', '', 1).isdigit()),
        'starts_with_digit': int(line and line[0].isdigit()),
        'ends_with_digit': int(line and line[-1].isdigit()),
        'num_spaces': line.count(' '),
    }

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    # Read image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    # OCR
    ocr_text = pytesseract.image_to_string(image)
    lines = preprocess_ocr_output(ocr_text)
    # Feature extraction
    features = [extract_features(line) for line in lines]
    features_df = pd.DataFrame(features)
    # Predict labels
    predicted_labels = clf.predict(features_df)
    # Combine lines and labels
    results = list(zip(lines, predicted_labels))
    # TODO: Group lines into structured test results as per your requirements
    return {"results": results}

def clean_ocr_lines(ocr_text):
    lines = ocr_text.split('\n')
    cleaned = []
    for line in lines:
        # Remove leading/trailing whitespace and non-printable characters
        line = ''.join(c for c in line if c.isprintable())
        line = line.strip()
        # Normalize case (choose one: upper or lower)
        line = line.upper()
        if line:  # Skip empty lines
            cleaned.append(line)
    return cleaned

def filter_lines(lines, min_len=2, max_len=50):
    filtered = []
    for line in lines:
        if min_len <= len(line) <= max_len and any(c.isalnum() for c in line):
            filtered.append(line)
    return filtered

def remove_duplicates(lines):
    seen = set()
    unique = []
    for line in lines:
        if line not in seen:
            unique.append(line)
            seen.add(line)
    return unique

def preprocess_ocr_output(ocr_text):
    lines = clean_ocr_lines(ocr_text)
    lines = filter_lines(lines)
    lines = remove_duplicates(lines)
    return lines