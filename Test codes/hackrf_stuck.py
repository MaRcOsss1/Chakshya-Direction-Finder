import subprocess
import time

def run_sweep():
    """Run HackRF sweep for 60 sweeps and return the max power detected."""
    print("Starting HackRF sweep for 60 sweeps...")

    process = subprocess.Popen(
        ["hackrf_sweep", "-f", "2400:2500", "-g", "40", "-N", "60"],  
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    time.sleep(7)  # Allow time for HackRF to start

    max_power = float('-inf')  # Initialize lowest power

    for _ in range(60):  # Read 60 sweeps
        line = process.stdout.readline().strip()
        if not line:
            continue  # Skip empty lines

        parts = line.split(",")
        if len(parts) < 7:
            continue  # Skip invalid lines

        try:
            power_values = list(map(float, parts[6:]))  # Extract power readings
            current_max = max(power_values)  # Find max power in this sweep
            max_power = max(max_power, current_max)  # Update global max
        except ValueError:
            continue  # Ignore invalid data

    process.terminate()  # Stop HackRF sweep
    return max_power if max_power != float('-inf') else None  # Return max power

# 🔄 REPEATED PROCESS
while True:
    angle = input("\nEnter the antenna angle (degrees) or 'q' to quit: ").strip()
    if angle.lower() == 'q':
        break

    print(f"Scanning at {angle}°...")
    max_power = run_sweep()

    if max_power is None:
        print(f"No valid power data received for angle {angle}°! Try again.")
    else:
        print(f"Angle: {angle}°, Max Power: {max_power:.2f} dBm")

