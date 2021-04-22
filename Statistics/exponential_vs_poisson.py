#%%
import numpy as np

# Sample (exponential) TIME BETWEEN EVENTS
samples = np.random.exponential(scale=1/5, size=15_000)


# Using these, count how many events/minute there are
ev_per_min = []
for i in range(int(samples.sum())):
    ev_per_min.append(((samples.cumsum()<i)&(samples.cumsum()>(i-1))).sum())


# Draw real samples from poisson distribution
from scipy import stats as stats
real_samples = stats.poisson.rvs(5, size=2000)

# Visually compare them
import seaborn as sns
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
sns.histplot(ev_per_min, bins=range(0,20), color='red', ax=ax)
sns.histplot(real_samples, bins=range(0,20), color='green', ax=ax)