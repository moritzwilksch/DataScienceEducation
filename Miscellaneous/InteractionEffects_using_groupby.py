#%%
import pandas as pd
import seaborn as sns


#%%
# GROUP BY TARGET (if categorical)
df = sns.load_dataset('titanic')
print(df.groupby('survived').mean().T)

# AND BY CATEGORICAL FEATURES
for col in df.select_dtypes('category'):
    print(f"=== Grouping by {col} ===")
    print(df.groupby(col).mean().T)
    print()

#%%
# GROUP BY EVERY CATEGORICAL FEATURE
df = sns.load_dataset('tips')
df['tippct'] = df.tip/df.total_bill
for col in df.select_dtypes('category'):
    print(f"=== Grouping by {col} ===")
    print(df.groupby(col).mean().T)
    print()
