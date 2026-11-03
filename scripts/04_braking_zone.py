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

# Membaca data
with open(data_file, "r", encoding="utf-8") as file:
    raw = json.load(file)

df = pd.DataFrame(raw["tel"])
df = df.dropna(subset=["x", "y", "brake"])

# Memisahkan kondisi pengereman
braking = df[df["brake"] > 0]
not_braking = df[df["brake"] == 0]

# Visualisasi
plt.figure(figsize=(12, 8))

plt.scatter(
    not_braking["x"],
    not_braking["y"],
    color="green",
    s=8,
    label="No Braking"
)

plt.scatter(
    braking["x"],
    braking["y"],
    color="red",
    s=15,
    label="Braking"
)

plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Braking Zone - Lewis Hamilton")
plt.axis("equal")
plt.legend()
plt.grid(alpha=0.2)

plt.tight_layout()
plt.savefig(output_dir / "05_braking_zone.png", dpi=300)
plt.show()
 
print("Jumlah titik pengereman:", len(braking))
print("Jumlah titik tanpa pengereman:", len(not_braking))

print("\n=== BRAKE DATA CHECK ===")
print("Nilai brake:", sorted(df["brake"].dropna().unique()))
print("Nilai maksimum brake:", df["brake"].max())