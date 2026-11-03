import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Menentukan lokasi folder project
project_dir = Path(__file__).resolve().parent.parent

# Lokasi file data
data_file = project_dir / "data" / "22_tel.json"

# Lokasi penyimpanan grafik
output_dir = project_dir / "outputs"
output_dir.mkdir(exist_ok=True)

with open(data_file, "r", encoding="utf-8") as file:
    raw = json.load(file)

df = pd.DataFrame(raw["tel"])
df = df.dropna(subset=["time", "x", "y", "brake"])
df = df.sort_values("time").reset_index(drop=True)

# Deteksi awal pengereman
df["brake_event"] = (
    (df["brake"] == 1) &
    (df["brake"].shift(1, fill_value=0) == 0)
)

events = df[df["brake_event"]]

plt.figure(figsize=(12, 8))

# Jalur sirkuit
plt.plot(df["x"], df["y"], color="gray",
         linewidth=1, alpha=0.6, label="Racing Line")

# Titik awal pengereman
plt.scatter(events["x"], events["y"],
            color="red", s=80, label="Braking Start",
            zorder=3)

# Nomor event
for i, (_, row) in enumerate(events.iterrows(), start=1):
    plt.annotate(
        str(i),
        (row["x"], row["y"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=10
    )

plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Braking Event Mapping - Lewis Hamilton")
plt.axis("equal")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(output_dir / "06_braking_event_mapping.png", dpi=300)
plt.show()

print("Jumlah braking event:", len(events))

print("\n=== BRAKING EVENT COORDINATES ===")

print(
    events[["time", "speed", "distance", "x", "y"]]
    .round(2)
    .to_string(index=False)
)