import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

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

clf = RandomForestClassifier()
clf.fit(X_train, y_train)
print("Accuracy:", clf.score(X_test, y_test))

joblib.dump(clf, 'line_classifier.pkl')
