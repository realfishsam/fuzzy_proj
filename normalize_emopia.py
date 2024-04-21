import pandas as pd

df = pd.read_csv('EMOPIA_2.2/metadata_by_song.csv')
print(df.head())

print("Mean before normalization:")
print(df[['num_Q1', 'num_Q2', 'num_Q3', 'num_Q4']].mean())
print("\nStandard Deviation before normalization:")
print(df[['num_Q1', 'num_Q2', 'num_Q3', 'num_Q4']].std())

df['num_Q1'] = (df['num_Q1'] - df['num_Q1'].mean()) / df['num_Q1'].std()
df['num_Q2'] = (df['num_Q2'] - df['num_Q2'].mean()) / df['num_Q2'].std()
df['num_Q3'] = (df['num_Q3'] - df['num_Q3'].mean()) / df['num_Q3'].std()
df['num_Q4'] = (df['num_Q4'] - df['num_Q4'].mean()) / df['num_Q4'].std()

print("\nData after Z-score normalization:")
print(df.head())

print("\nMean after normalization:")
print(df[['num_Q1', 'num_Q2', 'num_Q3', 'num_Q4']].mean())
print("\nStandard Deviation after normalization:")
print(df[['num_Q1', 'num_Q2', 'num_Q3', 'num_Q4']].std())

df.to_csv('EMOPIA_2.2_normalized_metadata_by_song.csv', index=False)
