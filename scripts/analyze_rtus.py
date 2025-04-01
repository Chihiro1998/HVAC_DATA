import pandas as pd
import matplotlib.pyplot as plt
import os

# Load RTU data files
base_path = '../HVAC_NewData/'
rtu_files = {
    'RTU_1': pd.read_csv(base_path + 'RTU_1.csv', parse_dates=['time']),
    'RTU_2': pd.read_csv(base_path + 'RTU_2.csv', parse_dates=['time']),
    'RTU_3': pd.read_csv(base_path + 'RTU_3.csv', parse_dates=['time']),
}

# Ensure output directory exists
output_dir = '../outputs/rtu_activity_analysis/'
os.makedirs(output_dir, exist_ok=True)

# Plot and optionally save a specific metric for all RTUs
def plot_rtu_metric(metric: str, title: str, ylabel: str, save=True):
    plt.figure(figsize=(12, 5))
    plotted = False
    for name, df in rtu_files.items():
        if metric in df.columns and df[metric].notna().any():
            plt.plot(df['time'], df[metric], label=name)
            plotted = True
    if not plotted:
        print(f"[Warning] No valid data found for metric: {metric}")
        return
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save:
        filename = f"{output_dir}{metric}_over_time.png"
        plt.savefig(filename)
        print(f"[Saved] Plot saved to: {filename}")
    plt.show()

# Plot 3 key RTU metrics and save
plot_rtu_metric('SuplAirTemp', 'Supply Air Temperature Over Time', 'Temperature (°F)', save=True)
plot_rtu_metric('HtgPct', 'Heating Percentage Over Time', 'Heating Power (%)', save=True)
plot_rtu_metric('SuplFanSpd', 'Supply Fan Speed Over Time', 'Fan Speed (%)', save=True)
