
import pandas as pd

# Load the current file
df = pd.read_csv('december-chart-inputs.csv')

# Keep only original columns
original_columns = ['pickup', 'delivery', 'distance', 'equipment', 'weight', 'date', 'predicted_rate']
df_clean = df[original_columns]

# Save cleaned version
df_clean.to_csv('december-chart-inputs.csv', index=False)
print("Fixed december-chart-inputs.csv")
print(f"Columns: {df_clean.columns.tolist()}")
print(f"Shape: {df_clean.shape}")
