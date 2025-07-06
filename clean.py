import pandas as pd

# Load raw file with junk header
df = pd.read_csv("data/gld_hourly.csv", skiprows=2)

# Rename columns to standard order: date, open, high, low, close, volume
df.columns = ['date', 'close', 'high', 'low', 'open', 'volume']

# Reorder columns to match expected ML pipeline
df = df[['date', 'open', 'high', 'low', 'close', 'volume']]

# Save cleaned CSV
df.to_csv("gld_hourly_cleaned.csv", index=False)
print("✅ Cleaned CSV saved to: data/gld_hourly_cleaned.csv")
