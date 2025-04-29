import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

input_folder = "lbmaske"  # Your folder with images
output_folder = "ocr_texts"
os.makedirs(output_folder, exist_ok=True)

# If on Windows and Tesseract is not in PATH, specify the path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_folder, filename)
        text = pytesseract.image_to_string(Image.open(img_path))
        with open(os.path.join(output_folder, filename + ".txt"), "w", encoding="utf-8") as f:
            f.write(text)
