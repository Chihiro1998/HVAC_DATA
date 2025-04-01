import pandas as pd
from scipy.stats import zscore

# Step 1: Load result CSV
input_path = '../outputs/connection_mapping_analysis/Step2_MatchingResults.csv'
df = pd.read_csv(input_path)

# Step 2: Clean column names and values
df.columns = df.columns.str.strip()
df['RTU'] = df['RTU'].str.strip()

# Step 3: Pivot to get correlation and MSE per RTU side-by-side
pivot_corr = df.pivot(index='VAV', columns='RTU', values='Correlation')
pivot_mse = df.pivot(index='VAV', columns='RTU', values='MSE')

# Step 4: Build combined DataFrame
combined_df = pd.DataFrame({
    'VAV': pivot_corr.index,
    'Correlation_RTU_1': pivot_corr['RTU_1'],
    'Correlation_RTU_2': pivot_corr['RTU_2'],
    'MSE_RTU_1': pivot_mse['RTU_1'],
    'MSE_RTU_2': pivot_mse['RTU_2'],
})

# Step 5: Z-score normalization for Correlation and MSE
combined_df['Corr_Z_RTU_1'] = zscore(combined_df['Correlation_RTU_1'])
combined_df['Corr_Z_RTU_2'] = zscore(combined_df['Correlation_RTU_2'])
combined_df['MSE_Z_RTU_1'] = zscore(combined_df['MSE_RTU_1'])
combined_df['MSE_Z_RTU_2'] = zscore(combined_df['MSE_RTU_2'])

# Step 6: Compute composite score (Correlation - MSE)
combined_df['Score_RTU_1'] = combined_df['Corr_Z_RTU_1'] - combined_df['MSE_Z_RTU_1']
combined_df['Score_RTU_2'] = combined_df['Corr_Z_RTU_2'] - combined_df['MSE_Z_RTU_2']

# Step 7: Select the better RTU based on score
def choose_rtu(score1, score2, threshold=0.5):
    if abs(score1 - score2) < threshold:
        return 'Unclear'
    return 'RTU_1' if score1 > score2 else 'RTU_2'

combined_df['Likely_Connected_To'] = combined_df.apply(
    lambda row: choose_rtu(row['Score_RTU_1'], row['Score_RTU_2']), axis=1
)

# Step 8: Save result
output_path = '../outputs/connection_mapping_analysis/Step2_Connection_Mapping_Table.csv'
combined_df.to_csv(output_path, index=False)

print(f"Mapping table saved to: {output_path}")
