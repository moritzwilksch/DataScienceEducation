# %% [markdown]
# # Maximum Likelihood Estimation

# %%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
# %%
from scipy.stats import norm, rv_continuous
data = np.array([1, 2, 5, 6])  # test data


# %%
def get_lik(data, mu, sd):
    """ Returns likelihood of observing *data* given *mu* and *sigma* of a normal distribution """
    nd = norm(mu, sd)
    return np.prod(nd.pdf(data))


# %%

# Start values
mu = [1]
sigma = [3]
stepsize = 0.1

for i in range(1000):
    # Randomly propose an updated mu and sigma
    new_mu = mu[-1] + np.random.normal(0, stepsize, 1)[0]
    new_sigma = sigma[-1] + np.random.normal(0, stepsize, 1)[0]
    old_lik = get_lik(data, mu[-1], sigma[-1])
    new_lik = get_lik(data, new_mu, new_sigma)

    # if new likelihood > old likelihood, update params
    if new_lik > old_lik:
        mu.append(new_mu)
        sigma.append(new_sigma)
    else:  # keep old params
        mu.append(mu[-1])
        sigma.append(sigma[-1])
