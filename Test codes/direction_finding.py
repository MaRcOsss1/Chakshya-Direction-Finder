import subprocess
import pandas as pd
import os

EXCEL_FILE = "direction_finding.xlsx"

def run_sweep():
    """Run HackRF sweep for 20 sweeps and return the max power detected."""
    max_power = float('-inf')  # Initialize lowest power
    power_readings = []  # Store all power readings

    process = subprocess.Popen(
        ["hackrf_sweep", "-f", "2400:2500", "-g", "40", "-N", "20"],  # Perform 20 sweeps
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    for _ in range(20):  # Read 20 sweeps
        line = process.stdout.readline().strip()
        if not line:
            continue  # Ignore empty lines

        parts = line.split(",")  # Parse CSV output
        try:
            power_values = list(map(float, parts[6:]))  # Extract power readings
            current_max = max(power_values)  # Find max power in this sweep
            power_readings.append(current_max)  # Store for logging
            max_power = max(max_power, current_max)  # Update global max
        except ValueError:
            continue  # Ignore invalid data

    process.terminate()  # Stop HackRF sweep
    return max_power if max_power != float('-inf') else None, power_readings  # Return max power and all readings

def save_to_excel(angle, power_readings):
    """Save sweep results to an Excel sheet."""
    df_new = pd.DataFrame({"Angle (°)": [angle] * len(power_readings), "Power (dBm)": power_readings})

    if os.path.exists(EXCEL_FILE):  # Append to existing file
        df_existing = pd.read_excel(EXCEL_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new  # Create new file if not exists

    df_combined.to_excel(EXCEL_FILE, index=False)
    print(f"📄 Data logged to {EXCEL_FILE}")

# 🏹 Direction-Finding Process
cycles = 3  # Number of cycles
angle_power_map = {}  # Store max power at each angle

for cycle in range(1, cycles + 1):
    print(f"\n🌀 Cycle {cycle}/{cycles}")
    angle = input("Enter the antenna angle (degrees): ").strip()

    print(f"📍 Scanning at {angle}°...")
    max_power, power_readings = run_sweep()

    if max_power is None:
        print(f"⚠️ No valid power data received for angle {angle}°! Check HackRF.")
    else:
        angle_power_map[int(angle)] = max_power
        print(f"🎯 Angle: {angle}°, Max Power: {max_power:.2f} dBm")
        save_to_excel(int(angle), power_readings)  # Log data

# 🔍 Find best direction
if angle_power_map:
    best_angle = max(angle_power_map, key=angle_power_map.get)
    print(f"\n🔍 Probable Drone Direction: ~{best_angle}° with strongest signal: {angle_power_map[best_angle]:.2f} dBm\n")
else:
    print("\n❌ No valid data received! Check HackRF settings.\n")
