import pandas as pd

# Load metrics file
df = pd.read_csv('../outputs/connection_mapping_analysis/connection_metrics_table.csv')

# Clean RTU/VAV if needed
df['VAV'] = df['VAV'].str.strip()
df['RTU'] = df['RTU'].str.strip()

# Sort by Corr_Temp descending, MSE ascending
df_sorted = df.sort_values(by=['VAV', 'Corr_Temp', 'MSE_Temp'], ascending=[True, False, True])

# Pick top RTU for each VAV
final_df = df_sorted.groupby('VAV').first().reset_index()

# Save final connection table
final_df[['VAV', 'RTU']].to_csv('../outputs/connection_mapping_analysis/final_connection_table.csv', index=False)

print("Final connection table saved!")
