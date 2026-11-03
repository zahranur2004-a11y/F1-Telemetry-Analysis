# F1 Telemetry Analysis: Driving Behavior, Braking & Track Curvature

## Project Overview

This project explores Formula 1 telemetry data to analyze driving behavior, braking patterns, and track characteristics.

The analysis focuses on one qualifying lap from Lewis Hamilton during the **2021 São Paulo Grand Prix**, using telemetry data obtained from the TracingInsights dataset.

Python is used to process and analyze telemetry data, while Matplotlib is used to visualize circuit layout, speed distribution, braking events, and track curvature.

The project aims to demonstrate how telemetry data can be transformed into meaningful insights through data analysis and visualization.

## Dataset

- **Source:** [TracingInsights – 2021 F1 Telemetry Dataset](https://github.com/TracingInsights/2021)
- **Grand Prix:** 2021 São Paulo Grand Prix
- **Session:** Qualifying
- **Driver:** Lewis Hamilton (HAM)
- **Lap:** 22
- **Data points:** 581 telemetry samples
- **Format:** JSON

The dataset contains telemetry variables such as speed, throttle, brake, gear, distance, time, and X-Y coordinates.

## Tools & Technologies

- **Python** – Data processing and analysis
- **Pandas** – Data manipulation
- **NumPy** – Numerical calculations
- **Matplotlib** – Data visualization
- **VS Code** – Development environment

## Analysis Workflow

The analysis is divided into several stages:

1. **Data Loading & Inspection** – Load the JSON telemetry dataset and inspect its structure, variables, and data points.
2. **Circuit Mapping & Speed Visualization** – Visualize the circuit layout using X-Y coordinates and examine speed patterns throughout the lap.
3. **Driving Behavior Analysis** – Examine throttle and brake inputs to identify different driving conditions.
4. **Braking Event Detection** – Identify consecutive braking samples and determine individual braking events.
5. **Braking Event Mapping** – Map the starting points of detected braking events onto the circuit layout.
6. **Braking Duration Analysis** – Calculate the estimated duration, speed reduction, and distance covered during each detected braking event.
7. **Cornering Analysis** – Examine changes in vehicle heading to identify variations in driving direction.
8. **Track Curvature Analysis** – Estimate track curvature using telemetry coordinates and distance data.
9. **Driving Performance Analysis** – Compare speed and curvature across driving conditions and explore their relationship.

## Key Findings

The analysis produced the following findings:

- **Maximum Speed:** 325 km/h
- **Minimum Speed:** 89 km/h
- **Average Speed:** 225.21 km/h (sample average)
- **Detected Braking Events:** 7 events
- **Braking Samples:** 95 samples
- **Estimated Total Braking Duration:** 10.24 seconds
- **Driving Conditions:**
  - Throttle Applied: 481 samples
  - Braking: 95 samples
  - Coasting: 5 samples
- **Speed and Curvature Relationship:** Pearson correlation coefficient of -0.7584, indicating a strong negative linear correlation in the analyzed samples.

These findings provide an overview of the driver's speed patterns, braking behavior, and the relationship between vehicle speed and estimated track curvature.

## Limitations & Considerations

- **Single-Lap Analysis:** The analysis is based on one qualifying lap and does not represent the driver's overall performance across multiple laps or race sessions.
- **Braking Duration:** Braking duration is estimated from consecutive brake-active telemetry samples. The calculation may exclude transition intervals at the beginning and end of each braking event.
- **Coordinate Scaling:** X-Y coordinates are empirically scaled by a factor of 10 to approximately align the calculated track distance with telemetry distance. The original coordinate units have not been independently verified.
- **Curvature Estimation:** Track curvature is numerically estimated from discrete telemetry coordinates and may be affected by sampling intervals, coordinate scaling, and measurement variations.
- **Correlation:** The Pearson correlation describes the linear relationship between speed and estimated curvature in the analyzed samples. It does not establish a causal relationship.

## Project Structure

```text
F1/
├── data/
│   └── 22_tel.json
├── scripts/
│   ├── 01_load_telemetry.py
│   ├── 02_circuit_mapping.py
│   ├── 03_driving_analysis.py
│   ├── 04_braking_zone.py
│   ├── 05_braking_events.py
│   ├── 06_braking_event_mapping.py
│   ├── 07_braking_duration.py
│   ├── 08_cornering_analysis.py
│   ├── 09_track_curvature.py
│   └── 10_driving_performance.py
├── outputs/
│   └── Generated visualization files (.png)
└── README.md
```

## Installation & How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/zahranur2004-a11y/F1-Telemetry-Analysis.git
cd F1
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Required Libraries

```bash
pip install pandas numpy matplotlib
```

### 5. Run the Analysis Scripts

Run the scripts sequentially from the project root directory:

```bash
python scripts/01_load_telemetry.py
python scripts/02_circuit_mapping.py
python scripts/03_driving_analysis.py
python scripts/04_braking_zone.py
python scripts/05_braking_events.py
python scripts/06_braking_event_mapping.py
python scripts/07_braking_duration.py
python scripts/08_cornering_analysis