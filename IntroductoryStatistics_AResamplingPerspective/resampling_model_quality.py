#%%
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score
import matplotlib.pyplot as plt
import numpy as np
#%%
df = sns.load_dataset('tips')
df = pd.get_dummies(df)

#%%
X = df.drop('tip', axis=1)
y = df['tip']

ytrain: pd.DataFrame
xtrain, xtest, ytrain, ytest = train_test_split(X, y)
real_model = LinearRegression()
real_model.fit(xtrain, ytrain)
print("===== REAL MODEL =====")
r2_real_model = explained_variance_score(ytest, real_model.predict(xtest))
print(f"R^2 = {r2_real_model}")

#%%
random_r2s = []
for _ in range(1000):
    crap_model = LinearRegression()
    # Fit model to shuffeled targets to see the R^2 of models on RANDOM data
    crap_model.fit(xtrain, ytrain.sample(frac=1))
    random_r2s.append(explained_variance_score(ytest, crap_model.predict(xtest)))

random_r2s = np.array(random_r2s)
print("===== CRAP MODEL OF SHUFFELED TARGETS =====")
print(f"R^2 95CI: {np.round(np.percentile(random_r2s, (2.5, 97.5)), 4)}")
print(f"Resampled p-value of the REAL MODEL = {sum(random_r2s >= r2_real_model)/len(random_r2s)}")

#%%
sns.distplot(random_r2s)
plt.title(r"$R^2$ of models that fit the SHUFFELED targets ($n=1000$)")
plt.xlabel(r"$R^2$")
plt.show()
