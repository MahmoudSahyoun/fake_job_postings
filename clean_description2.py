import pandas as pd
import re

# Load the previously cleaned description file
input_path = "cleaned_description.xlsx"
output_path = "cleaned_description_v2.xlsx"

# Read the Excel file
df = pd.read_excel(input_path)

# Function to clean description text
def clean_text(text):
    if pd.isnull(text):
        return ""
    # Remove HTML entities, multiple spaces, and trim
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# Define patterns to flag
hype_words = ["world class", "cutting edge", "best work", "superb", "revolutionary", "life-changing"]
html_tag_pattern = re.compile(r"</?\w+[^>]*>")  # matches HTML-like tags

# Function to analyze a single description
def analyze_description(desc):
    clean_desc = clean_text(desc)
    word_count = len(clean_desc.split())
    has_hype = any(word.lower() in clean_desc.lower() for word in hype_words)
    has_html = bool(html_tag_pattern.search(desc)) if pd.notnull(desc) else False
    is_low_quality = word_count < 30 or "lorem" in clean_desc.lower()
    return pd.Series([clean_desc, word_count, has_hype, has_html, is_low_quality],
                     index=["clean_description", "description_word_count", "has_hype_words", "has_html_tags", "is_low_quality"])

# Apply the function to the DataFrame
results = df["description"].apply(analyze_description)

# Merge or replace columns safely
df[['clean_description', 'description_word_count', 'has_hype_words', 'has_html_tags', 'is_low_quality']] = results

# Save to new Excel file
df.to_excel(output_path, index=False)
print(f"✅ Cleaned and analyzed descriptions saved to: {output_path}")
