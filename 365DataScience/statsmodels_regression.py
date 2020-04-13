#%%
import seaborn as sns
import pandas as pd
import statsmodels.api as sm

#%%
df = sns.load_dataset('tips')
df = pd.get_dummies(df, drop_first=True)
df.head()

X = df.drop('tip', axis=1)
y = df.tip

#%%
model = sm.OLS(y, X)
results = model.fit()
results.summary()

#%%
from sklearn.linear_model import LinearRegression
lr = LinearRegression(normalize=True)
lr.fit(X, y)
pd.Series(lr.coef_, index=X.columns.values)