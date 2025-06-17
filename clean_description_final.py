import pandas as pd
import re

# Load your data
file_path = "cleaned_description_v2.xlsx"
df = pd.read_excel(file_path)

# Remove rows where clean_description is NaN
df = df[df['clean_description'].notna()]

# Drop duplicate clean_descriptions
df = df.drop_duplicates(subset='clean_description')

# Define list of stopphrases (extendable)
stopphrases = [
    "click here", "apply now", "visit our website", "http", "#url_", "#email_", "contact us"
]

# Function to check if any stopphrase is in the description
def contains_stopphrase(text):
    text = str(text).lower()
    return any(phrase in text for phrase in stopphrases)

# Apply stopphrase filter
df = df[~df['clean_description'].apply(contains_stopphrase)]

# Remove short descriptions (<= 30 words)
df = df[df['description_word_count'] > 30]

# Save to new file
output_path = "cleaned_description_final.xlsx"
df.to_excel(output_path, index=False)

print(f"✅ Final cleaned data saved to: {output_path}")
