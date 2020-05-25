#%%
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import numpy as np
#%%
df = sns.load_dataset('tips')
df['pct_tip'] = df['tip']/df['total_bill']
df['size'] = df['size'].astype('category')

#%%
for cat in df.select_dtypes('category'):
    _heading = f"================ Group by {cat} ================"
    print(_heading)
    g = df.groupby(cat)[['pct_tip', 'total_bill', 'tip']]
    print(g.mean())
    """if len(g.groups) == 2:
        a, b = g
        print(ttest_ind(a[1], b[1]))
"""
#%%
sns.pairplot(df, hue='time', diag_kind='kde', vars=df.select_dtypes(np.number).columns)
plt.show()

#%%
