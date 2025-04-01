import pandas as pd

# Load result CSV
input_path = '../outputs/connection_mapping_analysis/Step2_MatchingResults.csv'
df = pd.read_csv(input_path)

# Clean column names and RTU values (remove spaces, tabs, etc.)
df.columns = df.columns.str.strip()
df['RTU'] = df['RTU'].str.strip()

# Pivot to get RTU_1 and RTU_2 side-by-side
pivot_corr = df.pivot(index='VAV', columns='RTU', values='Correlation')
pivot_mse = df.pivot(index='VAV', columns='RTU', values='MSE')

def decide_connection(row_corr, row_mse):
    c1, c2 = row_corr.get('RTU_1'), row_corr.get('RTU_2')
    m1, m2 = row_mse.get('RTU_1'), row_mse.get('RTU_2')

    if pd.isna(c1) or pd.isna(c2) or pd.isna(m1) or pd.isna(m2):
        return 'Unclear'

    # If one correlation is at least 0.1 higher, take it
    if abs(c1 - c2) > 0.1:
        return 'RTU_1' if c1 > c2 else 'RTU_2'

    # If correlation similar, use MSE difference
    if abs(m1 - m2) > 30:
        return 'RTU_1' if m1 < m2 else 'RTU_2'

    # Otherwise unclear
    return 'Unclear'


# Construct final result DataFrame
result_df = pd.DataFrame({
    'VAV': pivot_corr.index,
    'Correlation_RTU_1': pivot_corr.get('RTU_1'),
    'Correlation_RTU_2': pivot_corr.get('RTU_2'),
    'MSE_RTU_1': pivot_mse.get('RTU_1'),
    'MSE_RTU_2': pivot_mse.get('RTU_2'),
})

# Apply decision logic
result_df['Likely_Connected_To'] = result_df.apply(
    lambda row: decide_connection(row[['Correlation_RTU_1', 'Correlation_RTU_2']],
                                  row[['MSE_RTU_1', 'MSE_RTU_2']]), axis=1)

# Save output table
output_path = '../outputs/connection_mapping_analysis/Step2_Connection_Mapping_Table.csv'
result_df.to_csv(output_path, index=False)
print(f"Connection mapping saved to: {output_path}")
