import pandas as pd
import re
import html

# === 1. Load the raw dataset ===
df = pd.read_csv("fake_job_postings.csv")

# === 2. Clean Title ===
def clean_title(t):
    if pd.isnull(t):
        return ""
    # lowercase & strip
    t = t.strip().lower()
    # remove any #URL_xxx# tokens
    t = re.sub(r"#url_[a-f0-9]+#", "", t, flags=re.IGNORECASE)
    # remove punctuation except hyphens
    t = re.sub(r"[^\w\s\-]", "", t)
    # collapse whitespace
    t = re.sub(r"\s+", " ", t).strip()
    return t

df['clean_title'] = df['title'].apply(clean_title)
df['title_word_count'] = df['clean_title'].apply(lambda x: len(x.split()))

# === 3. Clean Benefits ===
def clean_benefits(b):
    if pd.isnull(b):
        return None, 0
    # unescape HTML entities (&amp;, etc.)
    text = html.unescape(b)
    # remove URL tokens
    text = re.sub(r"#URL_[a-f0-9]+#", "", text, flags=re.IGNORECASE)
    # normalize &amp;
    text = text.replace("&amp;", "&")
    # split on bullets, semicolons, or newlines
    parts = re.split(r"[•;\n\r]", text)
    # strip extra chars and drop empties
    parts = [p.strip(" .:-") for p in parts if p.strip()]
    # rejoin as uniform bullets
    cleaned = "\n".join(f"- {p}" for p in parts)
    return cleaned, len(parts)

df[['clean_benefits', 'benefit_count']] = df['benefits'].apply(
    lambda x: pd.Series(clean_benefits(x))
)

# === 4. Save the cleaned output ===
df_out = df[['job_id', 'title', 'clean_title', 'title_word_count',
             'benefits', 'clean_benefits', 'benefit_count']]
df_out.to_csv("cleaned_title_benefits.csv", index=False)

print("✅ cleaned_title_benefits.csv generated with clean_title, title_word_count, clean_benefits, and benefit_count.")
