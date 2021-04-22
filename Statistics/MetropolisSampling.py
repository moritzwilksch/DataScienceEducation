# %% [markdown]
# # Maximum Likelihood Estimation

# %%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# %%
from scipy.stats import norm
# data = np.array([1, 2, 5, 6])  # test data
data = np.random.normal(1, 0.5, 20)

# %%


def get_lik(data, mu, sd):
    """ Returns likelihood of observing *data* given *mu* and *sigma* of a normal distribution """
    return np.prod(norm.pdf(data, loc=mu, scale=sd))


# %%

# Start values
mu = [1]
sigma = [3]
stepsize = 0.1

for i in range(1000):
    # Randomly propose an updated mu and sigma (Metropolis sampling)
    new_mu = mu[-1] + np.random.normal(0, stepsize, 1)[0]
    new_sigma = sigma[-1] + np.random.normal(0, stepsize, 1)[0]
    old_lik = get_lik(data, mu[-1], sigma[-1])
    new_lik = get_lik(data, new_mu, new_sigma)

    if np.random.random() < (new_lik/old_lik):
        # Probability of updating (except when the new_mu is better, then always upgrade)
        # depends on *how much better* the new parameters are
        mu.append(new_mu)
        sigma.append(new_sigma)
    else:  # keep old params
        mu.append(mu[-1])
        sigma.append(sigma[-1])

# %% [markdown]
""" 
The probability of the parameter update always depends on how much the update would improve the parameters. In this case: If there is an improvement, always update. If there is not, do a coinflip, depending on which the paramters are still updated.
The Markov Chain part is that we jump to a different position with a propability p.
"""

# %%
plt.plot(mu, label="mu")
plt.plot(sigma, label="sigma")
plt.legend()
plt.show()

sns.distplot(mu)
plt.title("Mu")
plt.show()
sns.distplot(sigma)
plt.title("Sigma")
plt.show()
# %%
