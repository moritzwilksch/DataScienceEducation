# %%
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# generate fake data      (mu, sigma, size)
sample1 = np.random.normal(100, 3, 42)
sample2 = np.random.normal(110, 7, 58)
pooled = np.append(sample1, sample2)

_, axes = plt.subplots(2,1, sharex=True)
sns.distplot(sample1, ax=axes[0])
sns.distplot(sample2, ax=axes[1])
plt.show()

# %%
# MLE fit distribution
n1 = stats.norm(*stats.norm.fit(sample1))
n2 = stats.norm(*stats.norm.fit(sample2))

# %%
x = np.arange(75, 150,0.5)
plt.plot(x, n1.pdf(x))
plt.plot(x, n2.pdf(x), color="red")
plt.show()

# %%
# Calculate Probability of sample2 values being bigger than sample1 values
SAMPLESIZE = 100000
n1rvs = n1.rvs(SAMPLESIZE)
n2rvs = n2.rvs(SAMPLESIZE)

avg_diff = np.mean(n2rvs - n1rvs)

print(f"P(n2 > n1) = \t\t\t{np.sum(n2rvs > n1rvs)/SAMPLESIZE}")
print(f"Average Difference (n2-n1) = \t{avg_diff}")

# %%
