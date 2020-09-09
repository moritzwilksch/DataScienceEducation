#%%
import seaborn as sns
sns.set_style('ticks')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = sns.load_dataset('tips')

"""group_a = df.query("day=='Thur'")['tip']
group_b = df.query("day=='Sun'")['tip']
"""

group_a = df.query("time=='Lunch'")['tip']
group_b = df.query("time=='Dinner'")['tip']

sns.distplot(group_a)
sns.distplot(group_b)
plt.title("Distribution of Tips.")
plt.show()

#%%

# Number of Bootstraps doesn't really affect Credible Interval, ONLY ITS CONVERGENCE!
n_bootstraps = 1000

# Each sample drawn should be as big as the original sample (len(group_a))!!!!
# Drawing larger samples would narrow the resulting Credible Interval  thereby simulating
# what CI would result if the ORIGINAL SAMPLE HAD BEEN BIGGER TO BEGIN WITH!!!!!
# This can be used for minimum sample size estimation.
mean_a = np.mean(np.random.choice(group_a, (n_bootstraps, len(group_a))), axis=1)
mean_b = np.mean(np.random.choice(group_b, (n_bootstraps, len(group_b))), axis=1)

#%%
pp = pd.DataFrame({'a': mean_a, 'b': mean_b}).melt()
sns.pointplot(data=df, y='tip', x='time')
#%%
sns.barplot(data=df, x='day', y='tip', dodge=True, hue='sex')

#%%
import tensorflow as tf
tf.__version__