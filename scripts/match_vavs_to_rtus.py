import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import os

# Define base paths
base_path = '../HVAC_NewData/'
output_path = '../outputs/connection_mapping_analysis/'
os.makedirs(output_path, exist_ok=True)

# Automatically detect all VAV data files (exclude RTU files)
vav_files = [
    f for f in os.listdir(base_path)
    if f.endswith('.csv') and 'RTU' not in f
]

# Load RTU data (only keep time and SuplAirTemp)
rtu_files = {
    'RTU_1': pd.read_csv(base_path + 'RTU_1.csv', parse_dates=['time']),
    'RTU_2': pd.read_csv(base_path + 'RTU_2.csv', parse_dates=['time']),
}

# Preprocess RTU data
for name in rtu_files:
    rtu_df = rtu_files[name][['time', 'SuplAirTemp']].dropna()
    rtu_df = rtu_df.set_index('time').sort_index()
    rtu_files[name] = rtu_df

# Prepare list to collect results
results = []

# Analyze each VAV file against both RTUs
for vav_file in vav_files:
    vav_path = os.path.join(base_path, vav_file)
    try:
        # Load and preprocess VAV data
        vav_df = pd.read_csv(vav_path, parse_dates=['time'])
        vav_df = vav_df[['time', 'DschAirTemp']].dropna().set_index('time').sort_index()
    except Exception as e:
        print(f"Skipping {vav_file} due to error: {e}")
        continue

    # Compare with each RTU
    for rtu_name, rtu_df in rtu_files.items():
        combined = pd.merge(vav_df, rtu_df, left_index=True, right_index=True, how='inner')

        if not combined.empty:
            # Calculate Pearson correlation and Mean Squared Error
            corr = combined['DschAirTemp'].corr(combined['SuplAirTemp'])
            mse = mean_squared_error(combined['DschAirTemp'], combined['SuplAirTemp'])

            # Store the result
            results.append({
                'VAV': vav_file.replace('.csv', ''),
                'RTU': rtu_name,
                'Correlation': round(corr, 3),
                'MSE': round(mse, 2)
            })

            # Plot and save temperature comparison
            plt.figure(figsize=(10, 4))
            plt.plot(combined.index, combined['DschAirTemp'], label=f'{vav_file} DschAirTemp')
            plt.plot(combined.index, combined['SuplAirTemp'], label=f'{rtu_name} SuplAirTemp', alpha=0.7)
            plt.title(f'{vav_file} vs {rtu_name}')
            plt.xlabel('Time')
            plt.ylabel('Temperature (°F)')
            plt.legend()
            plt.tight_layout()

            plot_filename = f"{vav_file.replace('.csv','')}_vs_{rtu_name}.png"
            plt.savefig(os.path.join(output_path, plot_filename))
            plt.close()

# Save result table as CSV
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(output_path, 'Step2_MatchingResults.csv'), index=False)
print(f"All results saved to: {output_path}")
