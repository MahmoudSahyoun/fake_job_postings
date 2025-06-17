import pandas as pd
import re

# === 1. Load the improved requirements file ===
df = pd.read_csv("cleaned_requirements_v2.csv")

# === 2. Define checks ===

# 2.a No stray bullet characters (“•”) should remain
stray_bullets = df['improved_requirements'].str.contains('•', na=False).sum()

# 2.b No missing space after period: look for “.<Letter>” patterns
missing_space_after_period = df['improved_requirements'] \
    .str.contains(r'\.[A-Za-z]', regex=True, na=False).sum()

# 2.c No lowercase-uppercase concatenation: “aB” patterns
concat_issues = df['improved_requirements'] \
    .str.contains(r'[a-z][A-Z]', regex=True, na=False).sum()

# 2.d No colon+bullet patterns left
colon_bullet_issues = df['improved_requirements'] \
    .str.contains(r':\s*•', regex=True, na=False).sum()

# 2.e Count total rows and missing
total = len(df)
missing = df['improved_requirements'].isna().sum()

# === 3. Print summary ===
print("📝 Improved Requirements Test Summary")
print(f"• Total rows: {total}")
print(f"• Missing improved_requirements: {missing}\n")

print("🔍 Formatting issue counts (should all be 0):")
print(f"  - Stray bullets (“•”): {stray_bullets}")
print(f"  - Missing space after period: {missing_space_after_period}")
print(f"  - Lowercase-uppercase concatenation: {concat_issues}")
print(f"  - Colon+bullet patterns: {colon_bullet_issues}\n")

# === 4. Sample some entries for visual inspection ===
print("🎲 Sample of cleaned entries:\n")
sample = df.dropna(subset=['improved_requirements']).sample(5, random_state=42)
for idx, row in sample.iterrows():
    print("─" * 80)
    print(f"Job ID: {row['job_id']} — Title: {row['title']}")
    print(row['improved_requirements'])
    print()

# === 5. Exit code ===
if any([stray_bullets, missing_space_after_period, concat_issues, colon_bullet_issues]):
    print("❌ Some formatting issues remain. Please review the counts above.")
else:
    print("✅ All formatting checks passed!")
