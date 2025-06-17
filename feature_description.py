import pandas as pd
import re

# === 1. Load cleaned descriptions ===
df = pd.read_excel("cleaned_description_v2.xlsx")

# === 2. New feature: character count ===
df['description_char_count'] = df['clean_description'].apply(lambda txt: len(txt) if isinstance(txt, str) else 0)

# === 3. Number of sentences ===
# We'll approximate by counting periods, exclamation and question marks
df['num_sentences'] = df['clean_description'].apply(
    lambda txt: sum(txt.count(c) for c in ['.', '!', '?']) if isinstance(txt, str) else 0
)

# === 4. Punctuation counts ===
df['exclamation_count'] = df['clean_description'].apply(lambda txt: txt.count('!') if isinstance(txt, str) else 0)
df['question_count']    = df['clean_description'].apply(lambda txt: txt.count('?') if isinstance(txt, str) else 0)

# === 5. Uppercase ratio ===
def uppercase_ratio(txt):
    if not isinstance(txt, str) or len(txt) == 0:
        return 0.0
    total = len(txt)
    uppers = sum(1 for c in txt if c.isupper())
    return uppers / total

df['uppercase_ratio'] = df['description'].apply(uppercase_ratio)

# === 6. Presence of any number ===
df['has_number'] = df['clean_description'].apply(
    lambda txt: 1 if re.search(r'\d', str(txt)) else 0
)

# === 7. Save features ===
feature_cols = [
    'job_id',
    'description_char_count',
    'description_word_count',
    'num_sentences',
    'exclamation_count',
    'question_count',
    'uppercase_ratio',
    'has_number',
    'has_hype_words',
    'has_html_tags',
    'is_low_quality'
]

df[feature_cols].to_csv("description_features.csv", index=False)
print("✅ description_features.csv written with new description-based features.")
