import subprocess

# Start HackRF sweep process
process = subprocess.Popen(
    ["hackrf_sweep", "-f", "2400:2500", "-g", "40"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True, bufsize=1, universal_newlines=True
)

# Read and print output in real-time
try:
    while True:
        output = process.stdout.readline().strip()
        if output:
            print(f"📡 {output}")  # Print received data line-by-line
except KeyboardInterrupt:
    print("\n⚠️ Stopping HackRF Sweep...")
    process.terminate()  # Ensure proper cleanup
    process.wait()
