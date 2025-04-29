# Bajaj-QR-2-lab-report-analyser
├── main.py # FastAPI app (API endpoint logic)
├── model.py # Model training script
├── requirements.txt # Python dependencies
├── line_classifier.pkl # Trained ML model (generated after training)
├── README.md # Project documentation
├── train.xlsx # Labeled data for model training
├── lbmaske/ # Folder containing lab report images
├── ocr_texts/ # Folder for OCR output (optional)
└── ... # Other files (e.g., .gitignore, Dockerfile)

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/lab-report-extraction.git
cd lab-report-extraction
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

- **Windows:** [Download here](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH.
- **Linux:** `sudo apt-get install tesseract-ocr`
- **macOS:** `brew install tesseract`

### 4. (Optional) Prepare Training Data

- Place your labeled lines in `train.xlsx` (see format in this repo).
- Place your lab report images in the `lbmaske/` folder.

### 5. Train the Model (if needed)

```bash
python model.py
```
This will generate `line_classifier.pkl`.

### 6. Run the FastAPI Server

```bash
uvicorn main:app --reload
```
Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.

---

## 🛠️ Usage

- Use the `/get-lab-tests` endpoint to upload a lab report image (PNG/JPG).
- The API will return structured test data as shown above.

---

## 🧠 Model Details

- **OCR:** Tesseract extracts text from the uploaded image.

- **Feature Extraction:** Each line from the OCR output is processed to extract features such as length, digit/alpha counts, presence of units, decimal points, ranges, capitalization, and more.

- **Classification:** A RandomForest model (or similar classical ML model) predicts the type of each line (`test_name`, `test_value`, `test_unit`, `reference_range`, `other`).

- **Post-processing:** Lines are grouped into structured lab test entries. The system parses values and reference ranges, and calculates if the test value is out of range.

- **No LLMs:** The pipeline uses only classical ML and rule-based logic, ensuring compliance with competition rules.

---

## 🧩 Customization & Retraining

- **To retrain the model:**  
  1. Update or expand `train.xlsx` with more labeled lines.
  2. (Optionally) Enhance the `extract_features` function in `model.py` for better accuracy.
  3. Run `python model.py` to generate a new `line_classifier.pkl`.

- **To add new features or rules:**  
  - Edit the `extract_features` function or post-processing logic in `main.py` and `model.py`.

---

## 🐞 Troubleshooting

- **TesseractNotFoundError:**  
  Ensure Tesseract is installed and its path is set in your script:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- **500 Internal Server Error:**  
  Check the server logs for details. Common issues include missing model files, incorrect file uploads, or Tesseract not installed.

- **Model accuracy is low:**  
  - Label more data and retrain.
  - Add more features to `extract_features`.
  - Clean and preprocess OCR output more aggressively.

---

## 🙏 Acknowledgements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [FastAPI](https://fastapi.tiangolo.com/)
- [scikit-learn](https://scikit-learn.org/)
- [Pandas](https://pandas.pydata.org/)

---

## ✉️ Contact

For questions, suggestions, or contributions, please open an issue or contact [ac8453@srmist.edu.in].

---


