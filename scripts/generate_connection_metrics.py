import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

# Define paths
data_dir = '../HVAC_NewData/'
output_dir = '../outputs/connection_mapping_analysis/'
os.makedirs(output_dir, exist_ok=True)

# Load VAV file list (exclude RTU files)
vav_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and 'RTU' not in f]

# Load RTU data and keep relevant fields
rtu_files = {
    'RTU_1': pd.read_csv(os.path.join(data_dir, 'RTU_1.csv'), parse_dates=['time']),
    'RTU_2': pd.read_csv(os.path.join(data_dir, 'RTU_2.csv'), parse_dates=['time']),
}
for rtu_name in rtu_files:
    df = rtu_files[rtu_name]
    df = df[['time', 'SuplAirTemp', 'HtgPct']].dropna()
    rtu_files[rtu_name] = df.set_index('time').sort_index()

# Function to safely compute correlation
def safe_corr(series_a, series_b):
    if series_a.std() == 0 or series_b.std() == 0:
        return np.nan
    return series_a.corr(series_b)

# Prepare result storage
results = []

# Match each VAV against each RTU
for vav_file in vav_files:
    vav_name = vav_file.replace('.csv', '')
    try:
        vav_df = pd.read_csv(os.path.join(data_dir, vav_file), parse_dates=['time'])
        vav_df = vav_df[['time', 'DschAirTemp', 'HtgPct', 'AirFlow']].dropna()
        vav_df = vav_df.set_index('time').sort_index()
    except Exception as e:
        print(f"Skipping {vav_file} due to error: {e}")
        continue

    for rtu_name, rtu_df in rtu_files.items():
        merged = vav_df.join(rtu_df, how='inner', lsuffix='_VAV', rsuffix='_RTU')
        if merged.empty:
            continue

        result = {
            'VAV': vav_name,
            'RTU': rtu_name,
            'Corr_Temp': round(safe_corr(merged['DschAirTemp'], merged['SuplAirTemp']), 3),
            'MSE_Temp': round(mean_squared_error(merged['DschAirTemp'], merged['SuplAirTemp']), 2),
            'Corr_HtgPct': round(safe_corr(merged['HtgPct_VAV'], merged['HtgPct_RTU']), 3),
            'Corr_AirFlow_HtgPct': round(safe_corr(merged['AirFlow'], merged['HtgPct_RTU']), 3)
        }
        results.append(result)

# Save result table
results_df = pd.DataFrame(results)
output_file = os.path.join(output_dir, 'connection_metrics_table.csv')
results_df.to_csv(output_file, index=False)
print(f"Connection metric table saved to: {output_file}")
