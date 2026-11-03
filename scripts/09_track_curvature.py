import json
import pandas as pd
import numpy as np
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
df = df.dropna(subset=["time", "x", "y", "speed"])
df = df.sort_values("time").reset_index(drop=True)

# Menghitung perubahan posisi
dx = np.gradient(df["x"])
dy = np.gradient(df["y"])

# Menghitung perubahan arah lintasan
ddx = np.gradient(dx)
ddy = np.gradient(dy)

# Menghitung curvature
numerator = np.abs(dx * ddy - dy * ddx)
denominator = (dx**2 + dy**2)**1.5

df["curvature"] = numerator / denominator

print("=== TRACK CURVATURE ANALYSIS ===")
print("Jumlah titik:", len(df))
print("Curvature maksimum:", df["curvature"].max())
print("Curvature minimum:", df["curvature"].min())
print("Curvature rata-rata:", df["curvature"].mean())

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))

scatter = plt.scatter(
    df["x"],
    df["y"],
    c=df["curvature"],
    cmap="plasma",
    s=12
)

plt.colorbar(scatter, label="Track Curvature (1/m)")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Track Curvature Mapping - Lewis Hamilton")
plt.axis("equal")
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(output_dir / "09_track_curvature.png", dpi=300)
plt.show()

print("\n=== SHARPEST CORNER CANDIDATE ===")

top_points = df.nlargest(10, "curvature")

print(
    top_points[["time", "speed", "distance", "curvature"]]
    .round(4)
    .to_string(index=False)
)

plt.figure(figsize=(12, 5))

plt.plot(df["distance"], df["curvature"])

plt.xlabel("Distance (m)")
plt.ylabel("Curvature (1/m)")
plt.title("Track Curvature vs Distance")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("10_curvature_vs_distance.png", dpi=300)
plt.show()

print("\n=== CURVATURE AND SPEED CHECK ===")

correlation = df["curvature"].corr(df["speed"])

print("Korelasi curvature dan speed:", round(correlation, 4))