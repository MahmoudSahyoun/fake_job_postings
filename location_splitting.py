import pandas as pd

# === 1. Load the raw dataset ===
df = pd.read_csv("fake_job_postings.csv")

# === 2. Parse the 'location' column ===
# Split on commas into up to three parts
location_splits = df['location'].fillna("").str.split(",", n=2, expand=True)

# Strip whitespace and assign
df['country'] = location_splits[0].str.strip()
df['state']   = location_splits[1].str.strip()
df['city']    = location_splits[2].str.strip()

# === 3. Create a 'has_remote' flag from the 'telecommuting' column ===
# telecommuting==1 means remote friendly
df['has_remote'] = (df['telecommuting'] == 1).astype(int)

# === 4. (Optional) Drop the original 'location' and 'telecommuting' if you like ===
# df = df.drop(columns=['location', 'telecommuting'])

# === 5. Save the result ===
df[['job_id', 'location', 'country', 'state', 'city', 'telecommuting', 'has_remote']]\
    .to_csv("parsed_location.csv", index=False)

print("✅ parsed_location.csv written with country, state, city, and has_remote flag.")
