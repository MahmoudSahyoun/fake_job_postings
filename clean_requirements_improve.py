import pandas as pd
import re

# === 1. Load cleaned requirements file ===
input_path = "cleaned_requirements.csv"
df = pd.read_csv(input_path)

# === 2. Define the improvement function ===
def improve_requirements(text):
    if pd.isna(text):
        return text
    
    # 2.a Remove stray bullet characters
    text = text.replace('•', '')
    
    # 2.b Fix missing space after period: ".Word" -> ". Word"
    text = re.sub(r'\.([A-Za-z])', r'. \1', text)
    
    # 2.c Insert period between lowercase and uppercase when missing:
    # "vehicleValid" -> "vehicle. Valid"
    text = re.sub(r'([a-z])([A-Z])', r'\1. \2', text)
    
    # 2.d Normalize colon+bullet patterns: "Education:• " -> "Education: "
    text = re.sub(r':\s*•\s*', ': ', text)
    
    # 2.e Split into lines, strip, and ensure each starts with "- "
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if not line.startswith('- '):
            line = '- ' + line
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

# === 3. Apply improvements ===
df['improved_requirements'] = df['clean_requirements'].apply(improve_requirements)

# === 4. Save the updated file ===
output_path = "cleaned_requirements_v2.csv"
df.to_csv(output_path, index=False)

print(f"✅ Improved requirements saved to: {output_path}")
