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
df = df.dropna(subset=["time", "speed", "distance", "brake"])
df = df.sort_values("time").reset_index(drop=True)

# Identifikasi awal dan akhir pengereman
df["brake_event"] = (
    (df["brake"] == 1) &
    (df["brake"].shift(1, fill_value=0) == 0)
)

df["brake_end"] = (
    (df["brake"] == 1) &
    (df["brake"].shift(-1, fill_value=0) == 0)
)

starts = df[df["brake_event"]]
ends = df[df["brake_end"]]

results = []

for i, ((_, start), (_, end)) in enumerate(
    zip(starts.iterrows(), ends.iterrows()), start=1
):
    results.append({
        "Event": i,
        "Start Time": start["time"],
        "End Time": end["time"],
        "Duration": end["time"] - start["time"],
        "Start Speed": start["speed"],
        "End Speed": end["speed"],
        "Braking Distance": end["distance"] - start["distance"]
    })

result_df = pd.DataFrame(results)

print("=== BRAKING DURATION ANALYSIS ===")
print(result_df.round(2).to_string(index=False))

print("\nTotal braking duration:",
      round(result_df["Duration"].sum(), 2), "seconds")