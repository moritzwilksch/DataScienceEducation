# %%
import scipy.stats as stats
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %%
# Sample Size
n_m = 1000
n_f = 3440

# Conversion Rates
_mcr = 0.13
_fcr = 0.16

# Setup Data
sex = ['m'] * n_m + ['f'] * n_f
m_convert = np.random.choice((0, 1), p=(1 - _mcr, _mcr), size=n_m)
f_convert = np.random.choice((0, 1), p=(1 - _fcr, _fcr), size=n_f)
df = pd.DataFrame({'sex': sex, 'convert': np.append(m_convert, f_convert)})
df['convert'] = df['convert'].astype('category')

# Setup contingency table
ct = pd.crosstab(df.sex, df.convert)

# Output results
print(f'==== CROSSTAB ====\n{ct}')
print(f"==== TEST RESULTS ====")
print(f"---- Expected Results ----")
print(stats.chi2_contingency(ct)[3])
print(f"p = {stats.chi2_contingency(ct)[1]}")

#%%
# NOW: Bootstrapping Conversion Rate
niter=10000
m_bdist = stats.beta(sum(m_convert == 1), sum(m_convert == 0))
sns.distplot(m_bdist.rvs(niter), color='b', label='fitted distribution')
sns.distplot([np.random.choice(m_convert, size=len(m_convert)).mean() for _ in range(niter)], color='red',
             label='choice')

f_bdist = stats.beta(sum(f_convert == 1), sum(f_convert == 0))
sns.distplot(f_bdist.rvs(niter), color='g', label='fitted distribution')
sns.distplot([np.random.choice(f_convert, size=len(f_convert)).mean() for _ in range(niter)], color='y',
             label='choice')
plt.show()

#%%
mbscr = np.array([np.random.choice(m_convert, size=len(m_convert)).mean() for _ in range(niter)])
fbscr = np.array([np.random.choice(f_convert, size=len(f_convert)).mean() for _ in range(niter)])