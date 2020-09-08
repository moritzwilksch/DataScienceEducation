#%%
# This code uses a CALLBACK, NOT the lr_finder pip package!

import pandas as pd
import seaborn as sns
import numpy as np
import keras
from sklearn.model_selection import train_test_split
import tensorflow as tf
tf.random.set_seed(42)
from numpy.random import seed
seed(42)

#%%
df = sns.load_dataset('tips')
xtrain, xval, ytrain, yval = train_test_split(pd.get_dummies(df).drop('tip', axis=1), df.tip)

xtrain = xtrain.values
ytrain = ytrain.values
xval = xval.values
yval = yval.values

#%%
nn = keras.Sequential([
    keras.layers.Dense(units=15, activation='relu'),
    keras.layers.Dense(units=5, activation='relu'),
    keras.layers.Dense(units=1, activation='linear'),
])

nn.compile(keras.optimizers.Adam(lr=0.01), 'MAE', metrics=['MAE'])

# Find optimal learning rate. Use the one with the steepest descent of loss (not minimum)
from lr_finder import LRFinder
lrf = LRFinder(0.0001, 1)
nn.fit(xtrain, ytrain, validation_data=(xval, yval), epochs=5, batch_size=32, callbacks=[lrf])

#%%
h = nn.fit(xtrain, ytrain, validation_data=(xval, yval), epochs=25, batch_size=32)
pd.DataFrame({'train': h.history['loss'], 'val': h.history['val_loss']}).plot()

#%%
# Feature Importance
start_metric = nn.evaluate(xtrain, ytrain)[-1]
diffs = []
for colidx in range(xtrain.shape[1]):
    shuffled = xtrain.copy()
    np.random.shuffle(shuffled[:, colidx])
    shuff_metric = nn.evaluate(shuffled, ytrain)[-1]
    diffs.append(shuff_metric - start_metric)

pd.Series(diffs, index=pd.get_dummies(df).drop('tip', axis=1).columns).plot(kind='barh')

#%%