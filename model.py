import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.feature_extraction.text import CountVectorizer

# Replace 'labeled_lines.xlsx' with your actual file name
df = pd.read_excel('train.xlsx')

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

features = df['line_text'].apply(extract_features)
features_df = pd.DataFrame(features.tolist())

# Remove rows with NaN in features or labels
features_df = features_df.dropna()
df = df.loc[features_df.index]  # Keep labels in sync

data = pd.concat([features_df, df['label']], axis=1).dropna()
X = data[features_df.columns]
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = CountVectorizer()
X_text = vectorizer.fit_transform(df['line_text'].astype(str))
# Combine X_text with your custom features (use scipy.sparse.hstack)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)
print("Accuracy:", clf.score(X_test, y_test))

# Get test lines
test_indices = X_test.index
test_lines = df.loc[test_indices, 'line_text']

# Predict and print
predicted_labels = clf.predict(X_test)
for line, label in zip(test_lines, predicted_labels):
    print(f"{label}: {line}")

joblib.dump(clf, 'line_classifier.pkl')
import re

def parse_reference_range(ref_range):
    # Example: "12.0-15.0"
    match = re.match(r"([0-9.]+)-([0-9.]+)", ref_range)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

structured_data = []
current_test = {}

for line, label in zip(test_lines, predicted_labels):
    if label == "test_name":
        if current_test:  # Save previous test if exists
            structured_data.append(current_test)
        current_test = {"test_name": line}
    elif label == "test_value":
        current_test["test_value"] = line
    elif label == "test_unit":
        current_test["test_unit"] = line
    elif label == "reference_range":
        current_test["bio_reference_range"] = line

# Add the last test
if current_test:
    structured_data.append(current_test)

# Calculate lab_test_out_of_range
for test in structured_data:
    try:
        value = float(test.get("test_value", "nan"))
        ref_range = test.get("bio_reference_range", "")
        min_val, max_val = parse_reference_range(ref_range)
        test["lab_test_out_of_range"] = not (min_val <= value <= max_val)
    except Exception:
        test["lab_test_out_of_range"] = None  # or False

# Final output
output = {
    "is_success": True,
    "data": structured_data
}