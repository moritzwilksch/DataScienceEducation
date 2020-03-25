# %%
# Standard Imports
import keras
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
sns.set_style("ticks")

# %%
df = pd.read_csv('data/Audiobooks_data.csv', header=None,
                 names=[f"v{i}" for i in range(0, 12)])
df.head()

# %% [markdown]
"""# Balancing the dataset by removing 0-target rows.  
With Balancing: recall(0) = 0.84, recall(1) = 0.74  
Without Balancing: recall(0) = 1.0, recall(1) = 0.41  
"""
# %%
number_of_ones = sum(df['v11'] == 1)
g = df.groupby('v11')
df = g.apply(lambda group: group.sample(
    number_of_ones, replace=False)).reset_index(drop=True)
# %% [markdown]
# # Balancing the Dataset
# %%
X_unscaled = df.iloc[:, 1:-1]
y = df['v11']

# %% [markdown]
# # Scale Inputs
# %%
scaler = StandardScaler()
X = scaler.fit_transform(X_unscaled)

# %% [markdown]
# # Train Test Splitting

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# %%
model = keras.Sequential([
    keras.layers.Dense(units=20, input_dim=10, activation='tanh'),
    # keras.layers.Dense(units=50, activation='tanh'),
    keras.layers.Dense(units=1, activation='sigmoid')
])

model.compile('adam', 'binary_crossentropy')
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10,
          batch_size=32, callbacks=[keras.callbacks.EarlyStopping(patience=3)])

# %%
pd.DataFrame(model.history.history).plot()

# %%
print(classification_report(y_test, model.predict_classes(X_test)))
