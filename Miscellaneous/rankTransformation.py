#%%
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
#%%
dist = stats.lognorm(1,0)
rvs = dist.rvs(1000)
sns.distplot(rvs)
plt.title("RVS of Skewed Distribution")
plt.show()

#%%
m = rvs.mean()
sd = rvs.std()

standard_rvs = (rvs - m)/sd
sns.distplot(standard_rvs)
plt.title("Standardized RVS")
plt.show()

#%%

# Ranked RVS are now uniformly distributed
ranked_rvs = stats.rankdata(rvs)
sns.distplot(ranked_rvs)
plt.title("Ranked RVS")
plt.show()