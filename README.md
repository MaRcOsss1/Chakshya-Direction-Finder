# Chakshya-Direction-Finder

A direction-finding and signal intelligence tool using HackRF SDR, focused on the 2.4GHz spectrum.  
Developed by **Aryan Shah** for research in jamming detection, RF localization, and wireless telemetry monitoring.

---

## 🔍 Overview

This project enables real-time signal direction estimation using spectrum sweep data, visualizes estimated directions via GUI, and detects potential jamming activities.  
It also includes basic Wi-Fi Remote ID data acquisition tools.

---

## ✅ Features

- 📡 **2.4GHz Sweep Scanning**: Uses HackRF One to scan and log power levels across the Wi-Fi band.
- 🎯 **Signal Direction Estimation**: Estimates RF source direction from power peak data.
- 🖼️ **Tkinter-Based GUI**: Displays real-time direction vectors with live updates.
- ⚠️ **Jamming Signal Detection**: Monitors for abnormal patterns in sweep logs.
- 📶 **Wi-Fi RID Logging**: Collects nearby Wi-Fi drone RID packets for basic telemetry.

---

## 📦 Dependencies

- Python 3.8+
- Libraries: `tkinter`, `matplotlib`, `csv`, `openpyxl`
- GNU/Linux Bash environment
- HackRF Tools (especially `hackrf_sweep`)

Install dependencies using:
```bash
pip install matplotlib openpyxl
```

---

## 🚀 Usage

### 1. Run a Frequency Sweep

```bash
bash hackrf_sweep.sh
```

Captures spectrum from HackRF and saves it to `sweep.csv`.

### 2. Estimate Direction

```bash
python direction_finding.py
```

Processes `sweep.csv` to estimate RF signal direction.

### 3. Visualize with GUI

```bash
python DF_gui.py
```

Launches GUI to view vectors and estimated signal direction.

### 4. Detect Jamming

```bash
bash jamming1.sh
```

Flags jamming-like behavior in the 2.4GHz band.

### 5. Capture Wi-Fi RID Data

```bash
bash wifi_rid.sh
```

Logs telemetry info broadcasted by drones (if supported).

---

## 📊 Example Outputs

- **Sweep Data**: Power values across frequency
- **Estimated Direction**: Angle or relative orientation to RF source
- **GUI View**: Canvas with direction vector plotted
- **Jamming Log**: Terminal or CSV report

---

## 👤 Author

**Aryan Shah**

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
