# %%
# This code uses a CALLBACK, NOT the lr_finder pip package!

from pdpbox import pdp, get_dataset, info_plots
from keras.wrappers.scikit_learn import KerasRegressor
from lr_finder import LRFinder
from numpy.random import seed
import pandas as pd
import seaborn as sns
import numpy as np
import keras
from sklearn.model_selection import train_test_split
import tensorflow as tf
tf.random.set_seed(42)
seed(42)

# %%
df = sns.load_dataset('tips')
xtrain, xval, ytrain, yval = train_test_split(
    pd.get_dummies(df).drop('tip', axis=1), df.tip)

x_cols = xtrain.columns

xtrain = xtrain.values
ytrain = ytrain.values
xval = xval.values
yval = yval.values

# %%
nn = keras.Sequential([
    keras.layers.Dense(units=15, activation='relu'),
    keras.layers.Dense(units=5, activation='relu'),
    keras.layers.Dense(units=1, activation='linear'),
])

nn.compile(keras.optimizers.Adam(lr=0.01), 'MAE', metrics=['MAE'])

# Find optimal learning rate. Use the one with the steepest descent of loss (not minimum)
lrf = LRFinder(0.0001, 1)
nn.fit(xtrain, ytrain, validation_data=(xval, yval),
       epochs=5, batch_size=32, callbacks=[lrf])

# %%
h = nn.fit(xtrain, ytrain, validation_data=(
    xval, yval), epochs=25, batch_size=32)
pd.DataFrame({'train': h.history['loss'], 'val': h.history['val_loss']}).plot()

# %%
# Feature Importance
start_metric = nn.evaluate(xtrain, ytrain)[-1]
diffs = []
for colidx in range(xtrain.shape[1]):
    shuffled = xtrain.copy()
    np.random.shuffle(shuffled[:, colidx])
    shuff_metric = nn.evaluate(shuffled, ytrain)[-1]
    diffs.append(shuff_metric - start_metric)

pd.Series(diffs, index=pd.get_dummies(df).drop(
    'tip', axis=1).columns).plot(kind='barh')

# %%


def build_fn():
    nn = keras.Sequential([
        keras.layers.Dense(units=15, activation='relu'),
        keras.layers.Dense(units=5, activation='relu'),
        keras.layers.Dense(units=1, activation='linear'),
    ])
    nn.compile(keras.optimizers.Adam(lr=0.01), 'MAE', metrics=['MAE'])
    return nn


wrapped = KerasRegressor(build_fn=build_fn)

wrapped.fit(xtrain, ytrain, validation_data=(
    xval, yval), epochs=25, batch_size=32)

# %%
pdp_day = pdp.pdp_isolate(model=wrapped,
                          dataset=pd.DataFrame(xtrain, columns=x_cols),
                          model_features=x_cols,
                          feature='day_Thur day_Fri day_Sat day_Sun'.split())

pdp_size = pdp.pdp_isolate(model=wrapped,
                          dataset=pd.DataFrame(xtrain, columns=x_cols),
                          model_features=x_cols,
                          feature='size', num_grid_points=6)

pdp_sex = pdp.pdp_isolate(model=wrapped,
                          dataset=pd.DataFrame(xtrain, columns=x_cols),
                          model_features=x_cols,
                          feature=['sex_Male', 'sex_Female'])

pdp_smoker = pdp.pdp_isolate(model=wrapped,
                          dataset=pd.DataFrame(xtrain, columns=x_cols),
                          model_features=x_cols,
                          feature=['smoker_No', 'smoker_Yes'])

pdp_time = pdp.pdp_isolate(model=wrapped,
                          dataset=pd.DataFrame(xtrain, columns=x_cols),
                          model_features=x_cols,
                          feature=['time_Lunch', 'time_Dinner'])

pdp_bill = pdp.pdp_isolate(model=wrapped,
                          dataset=pd.DataFrame(xtrain, columns=x_cols),
                          model_features=x_cols,
                          feature='total_bill', num_grid_points=50,)


pdp.pdp_plot(pdp_day, 'days', plot_lines=True, center=False)
pdp.pdp_plot(pdp_size, 'size', plot_lines=True, center=False)
pdp.pdp_plot(pdp_bill, 'total bill', plot_lines=True, center=False)
pdp.pdp_plot(pdp_sex, 'sex', plot_lines=True, center=False)
pdp.pdp_plot(pdp_smoker, 'smoker', plot_lines=True, center=False)
pdp.pdp_plot(pdp_time, 'time', plot_lines=True, center=True)