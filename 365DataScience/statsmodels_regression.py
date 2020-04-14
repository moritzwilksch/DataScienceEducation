# %%
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import numpy as np

# %%
df = sns.load_dataset('tips')
df = pd.get_dummies(df, drop_first=True)
df.head()

X = df.drop('tip', axis=1)
y = df.tip

# %%
model = sm.OLS(y, X)
results = model.fit()
results.summary()

# %%
# Regression in sklearn
from sklearn.linear_model import LinearRegression

lr = LinearRegression(normalize=True)
lr.fit(X, y)
pd.Series(lr.coef_, index=X.columns.values)

# %%
# Using f_regression for p-values for single features
from sklearn.feature_selection import f_regression

fr = f_regression(X, y)  # Outputs array of shape (2, n_features) with f-values (first) and p-values (second)
print(pd.Series(np.round(fr[1], 3), index=X.columns, name='p_value'))
