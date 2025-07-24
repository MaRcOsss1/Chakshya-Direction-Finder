import subprocess
import pandas as pd
import os
import time
import tkinter as tk
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random

CSV_FILE = "direction_finding.csv"

class HackRFScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Prothapan Direction Finder")
        self.root.configure(bg='black')
        
        # Left control panel
        control_frame = tk.Frame(root, bg='black')
        control_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.angle_label = tk.Label(control_frame, text="Enter Antenna Angle (°):", bg='black', fg='white')
        self.angle_label.pack()
        
        self.angle_entry = tk.Entry(control_frame, bg='white', fg='black')
        self.angle_entry.pack()
        
        self.scan_button = tk.Button(control_frame, text="Start Scan", command=self.start_scan)
        self.scan_button.pack()
        
        # Scrollable output text area
        text_frame = tk.Frame(control_frame)
        text_frame.pack()
        self.output_text = tk.Text(text_frame, height=15, width=50, wrap=tk.WORD, bg='white', fg='black')
        self.scrollbar = tk.Scrollbar(text_frame, command=self.output_text.yview)
        self.output_text.config(yscrollcommand=self.scrollbar.set)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.best_direction_label = tk.Label(control_frame, text="Best Direction: N/A", bg='black', fg='white')
        self.best_direction_label.pack()
        
        self.angle_power_map = {}
        self.signal_data = {}
        
        # Right-side polar plot
        plot_frame = tk.Frame(root, bg='black')
        plot_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        self.ax.set_title("Signal Strength Direction Finder", color='white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack()
    
    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
    
    def run_sweep(self, angle):
        """Simulate HackRF sweep using random values."""
        power_readings = [random.uniform(-90, -30) for _ in range(60)]
        for power in power_readings:
            self.log(f"{angle}°: Power {power:.2f} dBm")
            time.sleep(0.05)  # Simulate real-time streaming
            
        max_power = max(power_readings)
        return max_power, power_readings
    
    def save_to_csv(self, angle, power_readings):
        df_new = pd.DataFrame({"Angle (°)": [angle] * len(power_readings), "Power (dBm)": power_readings})
        df_new.to_csv(CSV_FILE, mode="a", index=False, header=not os.path.exists(CSV_FILE))
        self.log(f"Data logged to {CSV_FILE}")
    
    def start_scan(self):
        angle = self.angle_entry.get().strip()
        if not angle.isdigit():
            self.log("Invalid angle! Enter a number.")
            return
        
        self.log(f"Scanning at {angle}°...")
        thread = Thread(target=self.scan_process, args=(int(angle),))
        thread.start()
    
    def scan_process(self, angle):
        max_power, power_readings = self.run_sweep(angle)
        
        self.angle_power_map[angle] = max_power
        if angle not in self.signal_data:
            self.signal_data[angle] = []
        self.signal_data[angle].append(max_power)
        
        self.log(f"Max Power at {angle}°: {max_power:.2f} dBm")
        self.save_to_csv(angle, power_readings)
        
        self.update_polar_plot()
        
        best_angle = max(self.angle_power_map, key=self.angle_power_map.get)
        self.best_direction_label.config(text=f"Best Direction: {best_angle}° ({self.angle_power_map[best_angle]:.2f} dBm)")
    
    def update_polar_plot(self):
        self.ax.clear()
        self.ax.set_title("Signal Strength Direction Finder", color='white')
        self.ax.scatter(0, 0, c='red', s=100, label="Receiver")
        
        if self.signal_data:
            for angle, power_list in self.signal_data.items():
                latest_power = power_list[-1]
                max_power = max(self.angle_power_map.values())
                min_power = min(self.angle_power_map.values())
                distance = 100 + (latest_power - min_power) * -10
                self.ax.scatter(np.radians(angle), distance, c='lime', edgecolors='k', s=50)
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = HackRFScanner(root)
    root.mainloop()

