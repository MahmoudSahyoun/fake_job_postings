import pandas as pd
import re

# === 1. Load cleaned titles ===
df = pd.read_csv("cleaned_title_benefits.csv")

# === 2. Basic length features ===
df['title_char_count'] = df['clean_title'].apply(len)
# title_word_count is already present

# === 3. Seniority / role-level flags ===
seniority_terms = {
    'junior': r'\bjunior\b',
    'senior': r'\bsenior\b',
    'manager': r'\bmanager\b',
    'director': r'\bdirector\b',
    'intern': r'\bintern\b',
    'lead': r'\blead\b',
}
for key, pattern in seniority_terms.items():
    df[f'has_{key}'] = df['clean_title']\
        .str.contains(pattern, case=False, na=False).astype(int)

# === 4. Remote work flag ===
remote_pattern = re.compile(r'\b(remote|work from home|telecommute|telecommuting)\b', flags=re.IGNORECASE)
df['has_remote'] = df['clean_title']\
    .apply(lambda x: 1 if remote_pattern.search(str(x)) else 0)

# === 5. Parentheses flag ===
df['has_parentheses'] = df['clean_title']\
    .str.contains(r'\(|\)', na=False).astype(int)

# === 6. Uppercase word count ===
def count_uppercase_words(t):
    return sum(1 for w in str(t).split() if w.isupper())

df['num_uppercase_words'] = df['title'].apply(count_uppercase_words)

# === 7. Save features ===
feature_cols = [
    'job_id',
    'title_char_count',
    'title_word_count',
] + [f'has_{k}' for k in seniority_terms] + [
    'has_remote',
    'has_parentheses',
    'num_uppercase_words'
]

df[feature_cols].to_csv("title_features.csv", index=False)
print("✅ title_features.csv written with new title-based features.")