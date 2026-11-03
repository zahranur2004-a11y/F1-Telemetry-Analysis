import json
import pandas as pd
from pathlib import Path

# Menentukan lokasi folder project
project_dir = Path(__file__).resolve().parent.parent

# Lokasi file data
data_file = project_dir / "data" / "22_tel.json"

with open(data_file, "r", encoding="utf-8") as file:
    raw = json.load(file)

df = pd.DataFrame(raw["tel"])
df = df.dropna(subset=["time", "brake"])
df = df.sort_values("time").reset_index(drop=True)

# Mendeteksi awal pengereman
df["brake_event"] = (
    (df["brake"] == 1) &
    (df["brake"].shift(1, fill_value=0) == 0)
)

# Mengambil titik awal setiap pengereman
events = df[df["brake_event"]].copy()

print("=== BRAKING EVENT ANALYSIS ===")
print("Jumlah braking event:", len(events))

print("\nWaktu awal pengereman:")
print(events[["time", "speed", "distance"]].to_string(index=False))