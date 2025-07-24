import subprocess

process = subprocess.Popen(["hackrf_sweep", "-f", "2400:2500", "-g", "40"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

for _ in range(10):  # Read first 10 lines
    print(process.stdout.readline().strip())

process.terminate()
ccode
