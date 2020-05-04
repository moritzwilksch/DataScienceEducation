#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
from sklearn.tree import DecisionTreeClassifier

dtc = DecisionTreeClassifier()
dtc.fit(pd.get_dummies(df.drop('Churn', axis=1)), df.Churn)


#%%
sns.catplot(data=df, y='Churn', x='tdm_cat', kind='point', color='k')
plt.show()