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

df = df.dropna(
    subset=["time", "speed", "throttle", "brake", "x", "y"]
)

df = df.sort_values("time").reset_index(drop=True)

# Konversi koordinat dari 1/10 meter menjadi meter
df["x_m"] = df["x"] / 10
df["y_m"] = df["y"] / 10

# Validasi konsistensi jarak lintasan
df["distance_diff"] = df["distance"].diff()

# Menghitung perubahan koordinat
df["dx"] = df["x"].diff()
df["dy"] = df["y"].diff()

# Menghitung jarak berdasarkan koordinat
df["xy_distance"] = np.sqrt(
    df["dx"]**2 + df["dy"]**2
)

print("\n=== XY COORDINATE VALIDATION ===")

print("Rata-rata XY distance:", df["xy_distance"].mean())
print("Rata-rata telemetry distance:", df["distance_diff"].mean())

print("\n=== COORDINATE RANGE CHECK ===")

print("X minimum:", df["x"].min())
print("X maksimum:", df["x"].max())

print("Y minimum:", df["y"].min())
print("Y maksimum:", df["y"].max())

print("Distance total:", df["distance"].iloc[-1])

print("\n=== XY DISTANCE RATIO CHECK ===")

df["xy_ratio"] = (
    df["xy_distance"] / df["distance_diff"]
)

print("Rata-rata XY ratio:", df["xy_ratio"].mean())
print("Median XY ratio:", df["xy_ratio"].median())
print("Minimum XY ratio:", df["xy_ratio"].min())
print("Maximum XY ratio:", df["xy_ratio"].max())

print("\n=== COORDINATE SAMPLE CHECK ===")

print(
    df[
        ["time", "distance", "x", "y",
         "distance_diff", "xy_distance", "xy_ratio"]
    ].head(10).to_string(index=False)
)

print("\n=== XY RATIO DISTRIBUTION ===")

print(
    df["xy_ratio"].describe().round(4)
)

print("\nPersentase rasio antara 9 dan 11:")

valid_ratio = df["xy_ratio"].dropna()

percentage = (
    ((valid_ratio >= 9) & (valid_ratio <= 11)).mean()
    * 100
)

print(f"{percentage:.2f}%")

print("\n=== OUTLIER COORDINATE CHECK ===")

outliers = df[
    (df["xy_ratio"] < 9) |
    (df["xy_ratio"] > 11)
]

print("Jumlah outlier:", len(outliers))

print(
    outliers[
        ["time", "distance", "distance_diff",
         "xy_distance", "xy_ratio"]
    ].head(15).to_string(index=False)
)

print("\n=== TOTAL DISTANCE COMPARISON ===")

total_xy_distance = df["xy_distance"].sum()
total_telemetry_distance = df["distance_diff"].sum()

print("Total XY distance:", total_xy_distance)
print("Total telemetry distance:", total_telemetry_distance)

print(
    "Total ratio:",
    total_xy_distance / total_telemetry_distance
)

print("\n=== SCALED COORDINATE VALIDATION ===")

scaled_xy_distance = df["xy_distance"] / 10

print(
    "Total scaled XY distance:",
    scaled_xy_distance.sum()
)

print(
    "Average scaled XY distance:",
    scaled_xy_distance.mean()
)

print(
    "Average absolute error:",
    (scaled_xy_distance - df["distance_diff"]).abs().mean()
)

print("\n=== DISTANCE VALIDATION ===")

print("Jumlah jarak nol:", (df["distance_diff"] == 0).sum())
print("Jumlah jarak negatif:", (df["distance_diff"] < 0).sum())
print("Jarak minimum:", df["distance_diff"].min())
print("Jarak maksimum:", df["distance_diff"].max())
print("Rata-rata jarak:", df["distance_diff"].mean())

print("\n=== TOP 10 DISTANCE GAPS ===")

print(
    df.nlargest(10, "distance_diff")[
        ["time", "distance", "distance_diff", "speed"]
    ].to_string(index=False)
)

# Membandingkan jarak aktual dengan estimasi kecepatan
df["time_diff"] = df["time"].diff()

df["estimated_distance"] = (
    ((df["speed"] + df["speed"].shift(1)) / 2) / 3.6
) * df["time_diff"]

df["distance_error"] = (
    df["distance_diff"] - df["estimated_distance"]
)

print("\n=== DISTANCE VS SPEED VALIDATION ===")

print("Rata-rata error:",
      df["distance_error"].abs().mean())

print("Maksimum error:",
      df["distance_error"].abs().max())

# Menghitung curvature berdasarkan jarak lintasan
s = df["distance"].to_numpy()
x = df["x_m"].to_numpy()
y = df["y_m"].to_numpy()

dx = np.gradient(x, s)
dy = np.gradient(y, s)

ddx = np.gradient(dx, s)
ddy = np.gradient(dy, s)

numerator = np.abs(dx * ddy - dy * ddx)
denominator = (dx**2 + dy**2)**1.5

df["curvature"] = numerator / denominator

print("\n=== CURVATURE VALIDATION ===")

print("Jumlah NaN:", df["curvature"].isna().sum())
print("Jumlah Inf:", np.isinf(df["curvature"]).sum())
print("Jumlah nilai negatif:", (df["curvature"] < 0).sum())

print("Curvature minimum:", df["curvature"].min())
print("Curvature maksimum:", df["curvature"].max())

# Menghitung perubahan kecepatan
df["speed_change"] = df["speed"].diff()

# Menghitung kategori kondisi berkendara
df["driving_condition"] = np.select(
    [
        df["brake"] == 1,
        (df["brake"] == 0) & (df["throttle"] > 0),
    ],
    [
        "Braking",
        "Throttle Applied",
    ],
    default="Coasting"
)

print("\n=== CURVATURE STATISTICS ===")

print(df["curvature"].describe())

print("\nTop 10 curvature tertinggi:")
print(
    df.nlargest(10, "curvature")[
        ["time", "distance", "speed", "curvature", "driving_condition"]
    ]
)

print("\n=== CURVATURE PEAK DETAILS ===")

print(
    df.nlargest(10, "curvature")[
        ["time", "distance", "x_m", "y_m",
         "speed", "curvature"]
    ].to_string(index=False)
)

print("=== DRIVING PERFORMANCE CHECK ===")

print("\nJumlah titik setiap kondisi:")
print(df["driving_condition"].value_counts())

print("\nRata-rata kecepatan setiap kondisi:")
print(df.groupby("driving_condition")["speed"].mean().round(2))

print("\nRata-rata curvature setiap kondisi:")
print(df.groupby("driving_condition")["curvature"].mean().round(5))

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))

scatter = plt.scatter(
    df["x_m"],
    df["y_m"],
    c=df["curvature"],
    cmap="turbo",
    s=12
)

plt.colorbar(scatter, label="Curvature")
plt.scatter(
    [-360.6, -392.374],
    [335, 103.105],
    color="red",
    marker="x",
    s=100,
    label="Curvature Peaks"
)

plt.xlabel("X Coordinate (m)")
plt.ylabel("Y Coordinate (m)")
plt.title("F1 Track Curvature Validation")
plt.axis("equal")
plt.legend()
plt.grid(True)
plt.savefig(output_dir / "11_curvature_validation.png", dpi=300)
plt.show()

print("\n=== CURVATURE PEAK LOCATION CHECK ===")

for d in [2325, 2721]:
    subset = df[
        (df["distance"] >= d - 30) &
        (df["distance"] <= d + 30)
    ]

    print(f"\nArea sekitar {d} meter:")
    print("Jumlah titik:", len(subset))
    print("Curvature maksimum:", subset["curvature"].max())
    print("Curvature rata-rata:", subset["curvature"].mean())
    print("Kecepatan rata-rata:", subset["speed"].mean())

print("\n=== CURVATURE-SPEED CORRELATION ===")

correlation = df["curvature"].corr(df["speed"])

print("Pearson correlation:", round(correlation, 4))

plt.figure(figsize=(10, 6))

plt.scatter(
    df["curvature"],
    df["speed"],
    alpha=0.6
)

plt.xlabel("Curvature")
plt.ylabel("Speed (km/h)")
plt.title("Relationship Between Track Curvature and Speed")

plt.grid(True)
plt.savefig(output_dir / "12_curvature_vs_speed.png", dpi=300)
plt.show()