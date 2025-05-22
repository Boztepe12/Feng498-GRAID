import pandas as pd

# Load the CSV file
df = pd.read_csv('soil_data.csv')

# Get max values for columns 'n', 'p', and 'k'
max_n = df['N'].max()
max_p = df['P'].max()
max_k = df['K'].max()

print(f"Max N: {max_n}")
print(f"Max P: {max_p}")
print(f"Max K: {max_k}")

min_n = df['N'].min()
min_p = df['P'].min()
min_k = df['K'].min()

print(f"Min N: {min_n}")
print(f"Min P: {min_p}")
print(f"Min K: {min_k}")