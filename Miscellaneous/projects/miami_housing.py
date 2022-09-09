#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.io import arff
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor

#%%
data = arff.loadarff("data/miami2016.arff")
df = pd.DataFrame(data[0])
df.head()

#%%
def fix_colnames(data: pd.DataFrame) -> pd.DataFrame:
    data.columns = [cname.lower() for cname in data.columns]
    return data.drop("parcelno", axis=1)


clean = df.pipe(fix_colnames)
clean

#%%
X = clean.drop("sale_prc", axis=1)
y = clean["sale_prc"]
xtrain, xtest, ytrain, ytest = train_test_split(X, y)

#%%
model = LGBMRegressor(n_estimators=10000, objective="mae")
model.fit(xtrain, ytrain, eval_set=(xtest, ytest), early_stopping_rounds=100)

#%%
train_preds = model.predict(xtrain)
test_preds = model.predict(xtest)

#%%
from lightgbm.plotting import plot_importance

plot_importance(model, importance_type="gain")

#%%
plt.scatter(ytrain, ytrain - train_preds)


#%%
np.log(clean["sale_prc"]).plot(kind="hist", bins=50)


#%%

y = 50
yhat = np.arange(1, 200, 1)
ymse = np.abs((y - yhat))
logymse = np.abs((np.log(y) - np.log(yhat)))

plt.plot(yhat, ymse)

#%%
plt.plot(yhat, logymse)


#%%
x = np.arange(10, 200)
y = x / 100 - 1
logy = np.log(x / 100)
plt.plot(x, y)
plt.plot(x, logy)


#%%
from lightgbm import LGBMRegressor

model = LGBMRegressor()
X = clean.drop("sale_prc", axis=1)
y = clean["sale_prc"]
model.fit(X, np.log(y))
preds = np.exp(model.predict(X))
#%%
from scipy.optimize import minimize


def mse(y, yhat):
    return np.mean((y - yhat) ** 2)


def criterion(c, y, yhat):
    return mse(y, yhat + c)


minimize(criterion, args=(y, preds), x0=0)

#%%
print(mse(y, preds))
print(mse(y, preds + 4401.06534318))
