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
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.dummy import DummyRegressor
from lightgbm import LGBMRegressor

#%%

df = sns.load_dataset("tips")

# Feature Engineering
df = df.assign(tip_pct=df["tip"] / df["total_bill"])

X = df.drop(["tip", "tip_pct"], axis=1)
y = df["tip_pct"]


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
            # HistGradientBoostingRegressor(
            #     loss="absolute_error",
            # ),
            # DecisionTreeRegressor()
            # DummyRegressor(strategy="mean"),
            LGBMRegressor(objective="mae", importance_type="gain"),
        ),
    ]
)

print(cross_val_score(pipeline, X, y, scoring="neg_mean_absolute_error").mean())
preds = cross_val_predict(pipeline, X, y)

#%%
pred_df = X.assign(pred=preds, true=y, diff=preds - y)
pred_df.sort_values("diff").tail(15)


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
PartialDependenceDisplay.from_estimator(
    pipeline["model"],
    _transformer.transform(X),
    features=["remainder__total_bill"],
    feature_names=_transformer.get_feature_names_out(),
)


#%%
from sklearn.inspection import partial_dependence

partial_dependence(
    pipeline["model"],
    X=pd.DataFrame(
        _transformer.transform(X), columns=_transformer.get_feature_names_out()
    ),
    features=["oe__day"],
)


#%%
from sklearn.pipeline import ma