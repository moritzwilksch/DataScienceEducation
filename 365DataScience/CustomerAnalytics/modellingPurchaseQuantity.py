# %%
# Standard Imports
from sklearn.metrics import explained_variance_score
from sklearn.linear_model import LinearRegression
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
sns.set_style("ticks")

# %% [markdown]
# # Loading Data and Models
# %%
df = pd.read_csv("data/purchase_data.csv")
scaler = pickle.load(open('models/scaler.pickle', 'rb'))
pca = pickle.load(open('models/pca.pickle', 'rb'))
km_pca = pickle.load(open('models/kmeans_pca.pickle', 'rb'))

features = df[['Sex', 'Marital status', 'Age', 'Education',
               'Income', 'Occupation', 'Settlement size']]
df_std = scaler.transform(features)
df_pca = pca.transform(df_std)
segments = km_pca.predict(df_pca)

df_pq = pd.concat([df, pd.get_dummies(segments, prefix='Segment')], axis=1)
df_pq = df_pq.query('Incidence == 1')

# Add Dummies for brand
brand_dummies = pd.get_dummies(df_pq['Brand'], prefix='Brand')
df_pq = pd.concat([df_pq.drop('Brand', axis=1), brand_dummies], axis=1)

# add price for each incidence
df_pq['price_incidence'] = (
    df_pq.Brand_1 * df_pq.Price_1 +
    df_pq.Brand_2 * df_pq.Price_2 +
    df_pq.Brand_3 * df_pq.Price_3 +
    df_pq.Brand_4 * df_pq.Price_4 +
    df_pq.Brand_5 * df_pq.Price_5
)

# promotion_incidence <=> 1 if chosen brand on promotion else 0
df_pq['promotion_incidence'] = (
    df_pq.Brand_1 * df_pq.Promotion_1 +
    df_pq.Brand_2 * df_pq.Promotion_2 +
    df_pq.Brand_3 * df_pq.Promotion_3 +
    df_pq.Brand_4 * df_pq.Promotion_4 +
    df_pq.Brand_5 * df_pq.Promotion_5
)

# %% [markdown]
# # Modelling
# %%
X = df_pq[['price_incidence', 'promotion_incidence']]
y = df_pq['Quantity']

model_quantity = LinearRegression()
model_quantity.fit(X, y)

pd.DataFrame(model_quantity.coef_, index=X.columns, columns=['slope'])
# %%
print(f"R^2 = {explained_variance_score(y, model_quantity.predict(X))}")
# %% [markdown]
# This is quite a bad, simpified model, but due non-usable data in the Last_Inc_Quantity column there are only few predictors.