import json
import pandas as pd
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent / "data" / "22_tel.json"

with open(file_path, "r", encoding="utf-8") as file:
    raw = json.load(file)

telemetry = raw["tel"]
df = pd.DataFrame(telemetry)

print("Data berhasil dibaca!")
print(df.head())
print("\nUkuran data:", df.shape)
print("\nKolom:", df.columns.tolist())