# %%
from optuna.integration.tfkeras import TFKerasPruningCallback
import optuna
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras import Input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import MeanSquaredError
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=1000, n_features=20,
                           n_informative=5, n_redundant=10,
                           random_state=42)

# scale data between 0 and 1
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

print(X.shape)
print(y.shape)


# %%

encoding_dim = 2


def objective(trial):
    act = trial.suggest_categorical('act', ['relu', 'sigmoid', 'tanh'])

    layerin = Input(name='input', shape=(X.shape[-1],))
    hidden = Dense(trial.suggest_int('n_hidden_units_enc1', 10, 64, 8), activation=act)(layerin)
    hidden = Dense(trial.suggest_int(f'n_hidden_units_enc2', 4, 64, 8), activation=act)(hidden)
    dense = Dense(name='encoded', units=2, activation='linear')(hidden)  # tanh oder linear or relu or elu all work ok-ish
    layerout = Dense(units=X.shape[-1])(dense)  # (hidden_decode)

    model = Model(layerin, layerout)
    model.compile(trial.suggest_categorical('optim', ['adam', 'rmsprop', 'sgd']), 'mean_squared_error')
    model.fit(x=X, y=X, epochs=150, batch_size=32, callbacks=[EarlyStopping(patience=5, monitor='loss'), TFKerasPruningCallback(trial, 'loss')])
    return MeanSquaredError()(X, model.predict(X))


study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=10)

#%%
study.trials_dataframe().sort_values('value')
# %%
from optuna.visualization import plot_parallel_coordinate

plot_parallel_coordinate(study)

#%%
from optuna.importance import get_param_importances

get_param_importances(study)

#%%
import hiplot as hip

hip.Experiment.from_dataframe(study.trials_dataframe()).display()