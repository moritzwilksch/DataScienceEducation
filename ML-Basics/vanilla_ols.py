#%%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import HistGradientBoostingRegressor

#%%

df = sns.load_dataset("tips")

# Feature Engineering
df = df.assign(weekend=df["day"].isin(["Sat", "Sun"]))

X = df.drop("tip", axis=1)
# y = np.log(df["tip"])
y = df["tip"]

#%%
sns.boxplot(data=df, x="size", y="tip")
sns.displot(y)


#%%

CATCOLS = ["sex", "smoker", "day", "time"]
_transformer = ColumnTransformer(
    [
        # ("ohe", OneHotEncoder(drop="first"), ["sex", "smoker", "day", "time"]),
        ("oe", OrdinalEncoder(), CATCOLS),
    ],
    remainder="passthrough",
)

pipeline = Pipeline(
    [
        ("transformer", _transformer),
        # ("model", LinearRegression()),
        (
            "model",
            HistGradientBoostingRegressor(
                loss="absolute_error",
            ),
        ),
    ]
)

print(cross_val_score(pipeline, X, y, scoring="neg_mean_absolute_error").mean())
preds = cross_val_predict(pipeline, X, y)

#%%
# sns.scatterplot(x=y, y=preds - y, hue=df.day)
sns.kdeplot(preds - y, hue=df.day)
print(mean_absolute_error(y, preds))

# sns.scatterplot(x=np.exp(y), y=np.exp(preds))
# print(mean_absolute_error(np.exp(y), np.exp(preds)))

#%%
import plotly.express as px

plotdf = df.assign(resid=preds - y)
px.scatter(data_frame=plotdf, x="tip", y="resid", hover_data=plotdf.columns, color="day")

#%%
from sklearn.inspection import PartialDependenceDisplay

pipeline.fit(X, y)
PartialDependenceDisplay.from_estimator(pipeline, X, features=["day"])
