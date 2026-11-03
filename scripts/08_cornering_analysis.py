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

df = df.dropna(subset=["time", "speed", "x", "y"])
df = df.sort_values("time").reset_index(drop=True)

# Menghitung perubahan kecepatan
df["speed_change"] = df["speed"].diff()

# Menghitung perubahan posisi
df["dx"] = df["x"].diff()
df["dy"] = df["y"].diff()

# Menghitung perubahan arah lintasan
df["heading"] = pd.Series(
    __import__("numpy").degrees(
        __import__("numpy").arctan2(df["dy"], df["dx"])
    )
)

df["heading_change"] = df["heading"].diff()

# Normalisasi perubahan sudut
df["heading_change"] = (
    (df["heading_change"] + 180) % 360
) - 180

print("\n=== NORMALIZED HEADING CHECK ===")
print("Maksimum:", df["heading_change"].max())
print("Minimum:", df["heading_change"].min())

print("=== CORNERING DATA CHECK ===")
print("Jumlah titik telemetry:", len(df))
print("Perubahan kecepatan maksimum:", df["speed_change"].max())
print("Perubahan kecepatan minimum:", df["speed_change"].min())
print("Perubahan arah maksimum:", df["heading_change"].max())
print("Perubahan arah minimum:", df["heading_change"].min())

plt.figure(figsize=(12, 8))

scatter = plt.scatter(
    df["x"],
    df["y"],
    c=df["heading_change"].abs(),
    cmap="plasma",
    s=12
)

plt.colorbar(scatter, label="Absolute Heading Change (degrees)")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Cornering Direction Change - Lewis Hamilton")
plt.axis("equal")
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(output_dir / "08_cornering_mapping.png", dpi=300)
plt.show()