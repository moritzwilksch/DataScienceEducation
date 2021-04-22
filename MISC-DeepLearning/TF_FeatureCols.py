# %%
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import seaborn as sns
import pandas as pd
import tensorflow as tf
from tensorflow.python.feature_column.feature_column import InputLayer


# %%
df = sns.load_dataset('tips')

# TF Dataset cant handle strings. Only hand over numbers.
for catcol in ['sex', 'smoker', 'day', 'time']:
    df[catcol] = df[catcol].cat.codes


xtrain, xval, ytrain, yval = train_test_split(df.drop('tip', axis=1), df.tip)

# Standard-scale
ss = StandardScaler()
xtrain[['total_bill', 'size']] = ss.fit_transform(xtrain[['total_bill', 'size']])
xval[['total_bill', 'size']] = ss.transform(xval[['total_bill', 'size']])


# BOTH sets need to be batched somehow. Otherwise, .fit(...) crashes with "rank=0" error
trainset = tf.data.Dataset.from_tensor_slices((dict(xtrain), ytrain.values)).shuffle(buffer_size=len(xtrain)).batch(8)
valset = tf.data.Dataset.from_tensor_slices((dict(xval), yval.values)).batch(16)


# %%
emb_table = {
    'sex': 2,
    'smoker': 2,
    'day': 3,
    'time': 2,
}

# %%
feature_cols = []

for col in ['total_bill', 'size']:
    fc = tf.feature_column.numeric_column(col)
    feature_cols.append(fc)

for col in ['sex', 'smoker', 'day', 'time']:
    cat = tf.feature_column.categorical_column_with_vocabulary_list(col, vocabulary_list=xtrain[col].unique(), num_oov_buckets=1)
    emb = tf.feature_column.embedding_column(cat, dimension=emb_table[col], )
    feature_cols.append(emb)

#%%
model = tf.keras.Sequential([
    tf.keras.layers.DenseFeatures(feature_cols),
    tf.keras.layers.Dense(8, 'relu', kernel_regularizer=tf.keras.regularizers.l2()),
    #tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(8, 'relu', kernel_regularizer=tf.keras.regularizers.l2()),
    #tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(1, 'linear'),
])

#%%
mcp = tf.keras.callbacks.ModelCheckpoint('bestweights', save_best_only=True, save_weights_only=True)
model.compile(tf.keras.optimizers.Adam(), 'mean_absolute_error')
hist = model.fit(trainset, validation_data=valset, epochs=100, callbacks=[mcp])
model.load_weights("bestweights")

#%%
pd.DataFrame(hist.history).plot()

#%%
pd.DataFrame({'real': yval, 'pred': model.predict(valset).flatten()}).sample(25)

