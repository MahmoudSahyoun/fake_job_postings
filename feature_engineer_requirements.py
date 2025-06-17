import pandas as pd
import re

# === 1. Load cleaned requirements ===
df = pd.read_csv("cleaned_requirements_v2.csv")

# === 2. Define pattern lists ===
no_exp_patterns = [
    r'\bno experience\b',
    r'\bentry level\b',
    r'\bno prior experience\b',
    r'\bno previous experience\b',
    r'\btraining provided\b',
    r'\bno experience required\b',
]
no_deg_patterns = [
    r'\bno degree required\b',
    r'\bdegree not required\b',
    r'\bdegree optional\b',
]

# === 3. Compile regexes ===
no_exp_re = re.compile('|'.join(no_exp_patterns), flags=re.IGNORECASE)
no_deg_re = re.compile('|'.join(no_deg_patterns), flags=re.IGNORECASE)

# === 4. Base features: bullets, word counts, avg length ===
df['bullet_count'] = df['improved_requirements']\
    .apply(lambda txt: txt.count('\n') + 1 if pd.notnull(txt) else 0)
df['req_word_count'] = df['improved_requirements']\
    .apply(lambda txt: len(str(txt).split()))
df['avg_word_length'] = df['improved_requirements']\
    .apply(lambda txt: sum(len(w) for w in str(txt).split()) / max(len(str(txt).split()), 1))

# === 5. Degree flags ===
degrees = ['Bachelor', 'Master', 'PhD', 'Associate']
for deg in degrees:
    df[f'has_{deg.lower()}'] = df['improved_requirements']\
        .str.contains(deg, case=False, na=False).astype(int)

# === 6. Skill flags ===
skills = ['Python', 'SQL', 'Java', 'C++', 'Excel', 'JavaScript', 'AWS', 'Docker']
skill_cols = []
for skill in skills:
    # special case for C++
    if skill == 'C++':
        col = 'cpp'
        pattern = re.escape('C++')
    else:
        # normalize: lowercase and strip non-alphanumeric
        col = re.sub(r'[^0-9a-z]', '', skill.lower())
        pattern = re.escape(skill)
    skill_cols.append(f'has_{col}')
    df[f'has_{col}'] = df['improved_requirements']\
        .str.contains(pattern, case=False, na=False).astype(int)

# === 7. Experience extraction ===
def extract_years(txt):
    nums = re.findall(r'(\d+)\s+years?', str(txt), flags=re.IGNORECASE)
    nums = [int(n) for n in nums]
    return pd.Series({
        'min_experience': min(nums) if nums else 0,
        'max_experience': max(nums) if nums else 0
    })

exp_df = df['improved_requirements'].apply(extract_years)
df = pd.concat([df, exp_df], axis=1)

# === 8. No-experience & No-degree flags ===
df['no_experience_required'] = df['improved_requirements']\
    .fillna('')\
    .apply(lambda txt: 1 if no_exp_re.search(txt) else 0)

df['degree_not_required'] = df['improved_requirements']\
    .fillna('')\
    .apply(lambda txt: 1 if no_deg_re.search(txt) else 0)

# override experience when no_experience_required
df.loc[df['no_experience_required'] == 1, ['min_experience', 'max_experience']] = 0

# === 9. Save features ===
output_cols = [
    'job_id',
    'bullet_count', 'req_word_count', 'avg_word_length',
] + [f'has_{d.lower()}' for d in degrees] \
  + skill_cols \
  + ['min_experience', 'max_experience', 'no_experience_required', 'degree_not_required']

df[output_cols].to_csv("requirements_features_v2.csv", index=False)
print("✅ requirements_features_v2.csv written with all new features.")
