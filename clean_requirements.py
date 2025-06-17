import pandas as pd
import re

# Load original dataset
df = pd.read_csv("fake_job_postings.csv")

# Define stopphrases or noise segments to remove
stop_phrases = [
    "All information will be kept confidential",
    "according to EEOC guidelines",
    "Candidate must be eligible to work in the United States",
    "ADDITIONAL INFORMATION",
    "The Musts:", "The That’d Be Greats:",
    "Bonus Points:", "Bonus:",
    "Extra:", "Must be available",
    "MaxPlay and the Technicolor Ventures Group",
]

# Function to clean and structure the requirements
def clean_requirements(text):
    if pd.isna(text):
        return None

    # Remove HTML tags if any
    text = re.sub(r'<[^>]+>', '', text)

    # Normalize spacing
    text = re.sub(r'\s+', ' ', text.strip())

    # Remove known stop phrases
    for phrase in stop_phrases:
        text = text.replace(phrase, '')

    # Split on common bullet/requirement delimiters
    parts = re.split(r'[•\-\n\r;•]', text)

    # Clean each requirement
    parts = [p.strip(" .–:;") for p in parts if len(p.strip()) > 3]

    # Join back as clean bullet points
    return "\n".join(f"- {p}" for p in parts)

# Apply the cleaning function
df["clean_requirements"] = df["requirements"].apply(clean_requirements)

# Drop rows where requirements were originally missing
df_cleaned = df.dropna(subset=["clean_requirements"])

# Save cleaned output
df_cleaned.to_csv("cleaned_requirements.csv", index=False)
print("✅ Cleaned requirements saved to: cleaned_requirements.csv")
