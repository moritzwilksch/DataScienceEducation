#%%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# NOTATION ORDER
## Local MacBook 2015 1.2Ghz Intel Core M
## Always free GCP
## 8Cores/16GB GCP n1 instance

#%%
%%timeit
# 416 ms ± 31.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 213 ms ± 2.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 187 ms ± 1.38 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

df = sns.load_dataset('titanic')
sns.barplot(data=df, x='pclass', y='survived')
plt.savefig('/tmp/fig.png')
plt.close()

#%%
%%timeit
# 4.48 s ± 1.26 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 2.97 s ± 564 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 1.27 s ± 20.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
np.matmul(np.random.randint(0,99, (1000,1000)), np.random.randint(0,99, (1000,1000)))

#%%
%%timeit
# 69.5 ms ± 10 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 28 ms ± 657 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 19.9 ms ± 129 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
pd.pivot_table(data=df, index='age', columns='fare')

#%%
df['embark_town'] = df.embark_town.astype('string')
df = df.dropna()
#%%
%%timeit
# 1.23 ms ± 399 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 290 µs ± 3.95 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
# 260 µs ± 2.97 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
df['embark_town'].apply(lambda s: s[:2])

#%%
%%timeit
# 15.3 ms ± 1.32 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 3.68 ms ± 65.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 2.69 ms ± 10.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
df.groupby('fare').mean()