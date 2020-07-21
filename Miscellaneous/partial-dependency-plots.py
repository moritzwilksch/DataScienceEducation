# See https://christophm.github.io/interpretable-ml-book/pdp.html for details
#%%
import seaborn as sns
sns.set_style('ticks')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = sns.load_dataset('tips')
X = pd.get_dummies(df.drop('tip', axis=1))
y = df.tip

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(max_depth=3)
rf.fit(X, y)

#%%
from sklearn.inspection import plot_partial_dependence
plot_partial_dependence(rf, X, features=['total_bill', 'sex_Male', 'day_Sun'])