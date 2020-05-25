#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
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
sns.catplot(data=df, x='deck', y='survived', col='pclass', kind='bar')
plt.show()

#%%
sns.barplot(data=df, x='sex', y='survived', hue='pclass')
plt.show()

#%%
sns.catplot(data=df, col='sex', x='pclass', y='survived', kind='point', color='b')
plt.show()

#%%
# GROUP BY EVERY CATEGORICAL FEATURE
df = sns.load_dataset('tips')
df['tippct'] = df.tip/df.total_bill
for col in df.select_dtypes('category'):
    print(f"=== Grouping by {col} ===")
    print(df.groupby(col).mean().T)
    print()
#%%
df = pd.read_csv('/Users/Moritz/Desktop/telecom_churn.csv')
df.info()

#%%
sns.pointplot(data=df, x='Churn', y='Total day minutes')
plt.show()

#%%
# BEST: Plotting churn rate for serveral bins of Total day minutes
tmp = df.groupby(pd.cut(df['Total day minutes'], 10))['Churn'].mean()
tmp.index = [x.right for x in tmp.index]
sns.pointplot(x=tmp.index, y=tmp)
plt.show()
