import pandas as pd
import matplotlib.pyplot as plt

# === Load Excel File ===
df = pd.read_excel("cleaned_description_v2.xlsx")

# === 1. Check for NaNs ===
nan_rows = df[df['clean_description'].isna()]
print(f"🟡 NaN descriptions: {len(nan_rows)}")

# === 2. Check for Duplicate Descriptions ===
duplicates = df[df.duplicated('clean_description', keep=False)]
print(f"🔁 Duplicate descriptions: {len(duplicates)}")

# === 3. Check for Stopphrases ===
stop_phrases = ['#URL_', '#EMAIL_', '#NAME?', 'lorem ipsum', 'click here', 'apply now']

def contains_stopphrase(text):
    if pd.isna(text):
        return False
    return any(phrase.lower() in text.lower() for phrase in stop_phrases)

df['has_stopphrase'] = df['clean_description'].apply(contains_stopphrase)
stop_rows = df[df['has_stopphrase']]
print(f"🚫 Descriptions with stopphrases: {len(stop_rows)}")

# === 4. Plot Histogram of Word Counts ===
plt.figure(figsize=(10, 6))
plt.hist(df['description_word_count'], bins=25, edgecolor='black')
plt.title("📝 Word Count Distribution")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()

# === 5. Save All Flagged Issues ===
with pd.ExcelWriter("description_issues.xlsx") as writer:
    nan_rows.to_excel(writer, sheet_name='NaNs', index=False)
    duplicates.to_excel(writer, sheet_name='Duplicates', index=False)
    stop_rows.to_excel(writer, sheet_name='Stopphrases', index=False)

print("✅ Flagged issues saved to: description_issues.xlsx")

