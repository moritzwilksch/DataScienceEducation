#%%
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind

#%%
df = sns.load_dataset('tips')
df['pct_tip'] = df['tip']/df['total_bill']

#%%
for cat in df.select_dtypes('category'):
    _heading = f"================ Group by {cat} ================"
    print(_heading)
    g = df.groupby(cat)['pct_tip']
    print(g.mean())
    if len(g.groups) == 2:
        a, b = g
        print(ttest_ind(a[1], b[1]))
