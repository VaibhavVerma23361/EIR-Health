import pandas as pd
import json

# Load CSV
df = pd.read_csv("/home/ganesh/other/metri_kk/Tic_Tac_Tic/Tic-Tac-Toe/Home Remedies.csv")

# Replace NaN with empty strings
df = df.fillna("")

# Convert to JSON
json_data = df.to_dict(orient="records")

# Save cleaned JSON
json_path = "/home/ganesh/other/metri_kk/Tic_Tac_Tic/Tic-Tac-Toe/Home_remedies_clean.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)

print("✅ Clean JSON created at:", json_path)
