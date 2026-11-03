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

print("Memulai analisis telemetry...")

# Membaca data
with open(data_file, "r", encoding="utf-8") as file:
    raw = json.load(file)

df = pd.DataFrame(raw["tel"])
df = df.dropna(subset=["x", "y", "speed"])

print("Data berhasil dimuat!")
print("Jumlah titik:", len(df))

# Visualisasi lintasan
plt.figure(figsize=(12, 8))

scatter = plt.scatter(
    df["x"],
    df["y"],
    c=df["speed"],
    cmap="plasma",
    s=12
)

plt.colorbar(scatter, label="Speed (km/h)")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Hamilton - Sao Paulo GP 2021")
plt.axis("equal")
plt.grid(alpha=0.2)

plt.tight_layout()
plt.savefig(output_dir / "02_circuit_mapping.png", dpi=300)
plt.show()

# Statistik kecepatan
print("\n=== SPEED ANALYSIS ===")
print(f"Maximum: {df['speed'].max():.2f} km/h")
print(f"Minimum: {df['speed'].min():.2f} km/h")
print(f"Average: {df['speed'].mean():.2f} km/h")

# Grafik kecepatan terhadap waktu
plt.figure(figsize=(12, 5))

plt.plot(df["time"], df["speed"])

plt.xlabel("Time (seconds)")
plt.ylabel("Speed (km/h)")
plt.title("Hamilton - Speed vs Time")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "03_speed_vs_time.png", dpi=300)
plt.show()

print("\nAnalisis selesai!")