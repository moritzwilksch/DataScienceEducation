#%%
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

#%%
# generate linear x and y with random normal noise
x = np.linspace(0, 10, 100)
y = 2 * x + np.random.normal(0, 2, 100) + x ** 2 - 5 * x
plt.scatter(x, y)

#%%
# mean-center x and y
x_mc = x - np.mean(x)
y_mc = y - np.mean(y)

# standardize x and y
x_std = (x - x.mean()) / x.std()
y_std = (y - y.mean()) / y.std()

# fit linear regression model
model = smf.ols(formula="y ~ x", data={"x": x, "y": y})
# model = smf.ols(formula="y ~ x", data={"x": x_std, "y": y_std})
# model = smf.ols(formula="y ~ x", data={"x": x_mc, "y": y_mc})
results = model.fit()
print(results.summary())
residuals = results.resid

#%%
np.std(residuals)

# get predicted values
y_pred = results.predict()

plt.scatter(x, y_pred, color="blue")
plt.plot(x, y_pred + 1.96 * np.std(residuals), color="red")
plt.plot(x, y_pred - 1.96 * np.std(residuals), color="red")
plt.scatter(x, y, alpha=0.2, color="k")

#%%
# sklearn quantile regression 
from sklearn.linear_model import LinearRegression, QuantileRegressor
from sklearn.metrics import mean_squared_error

# fit quantile regressor
quantile = 0.05
for quantile in [0.05, 0.95]:
    qr = QuantileRegressor(quantile=quantile, alpha=0)
    qr.fit(x.reshape(-1, 1), y)
    y_pred = qr.predict(x.reshape(-1, 1))
    mse = mean_squared_error(y, y_pred)
    print(f"Quantile: {quantile}, MSE: {mse}")

    # plot x, y and predicted y
    plt.scatter(x, y)
    plt.plot(x, y_pred, color="red")
    print(qr.coef_, qr.intercept_)

#%%
