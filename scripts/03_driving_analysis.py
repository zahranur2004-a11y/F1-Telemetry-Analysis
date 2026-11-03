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

# Membaca telemetry
with open(data_file, "r", encoding="utf-8") as file:
    raw = json.load(file)

df = pd.DataFrame(raw["tel"])

# Membuat grafik throttle dan brake
fig, ax = plt.subplots(2, 1, figsize=(14, 8))

# Grafik throttle
ax[0].plot(
    df["time"],
    df["throttle"],
    color="green"
)

ax[0].set_title("Throttle vs Time")
ax[0].set_ylabel("Throttle (%)")
ax[0].grid(alpha=0.3)

# Grafik brake
ax[1].plot(
    df["time"],
    df["brake"],
    color="red"
)

ax[1].set_title("Brake vs Time")
ax[1].set_xlabel("Time (seconds)")
ax[1].set_ylabel("Brake")
ax[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / "04_throttle_brake.png", dpi=300)
plt.show()

print("\n=== DRIVING ANALYSIS ===")
print("Maximum throttle:", df["throttle"].max())
print("Jumlah titik brake aktif:", (df["brake"] > 0).sum())