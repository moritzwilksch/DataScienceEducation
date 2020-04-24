#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

#%%
# Load & Split Data
df = sns.load_dataset('titanic').fillna(method='ffill').drop('alive', axis=1)
df[['sex', 'embarked']] = df[['sex', 'embarked']].astype('category')
df = pd.get_dummies(df)
xtrain, xtest, ytrain, ytest = train_test_split(df.drop('survived', axis=1), df['survived'])

#%%
# BASELINE MODEL
baseline = LogisticRegression(max_iter=500, n_jobs=-1)
baseline.fit(xtrain, ytrain)
print(confusion_matrix(ytest, baseline.predict(xtest)))

#%%
# Train Tree
fare_discretizer = DecisionTreeClassifier(max_leaf_nodes=6)
fare_discretizer.fit(xtrain.fare.to_frame(), ytrain)

xtrain['fare'] = fare_discretizer.predict_proba(xtrain['fare'].to_frame())
xtest['fare'] = fare_discretizer.predict_proba(xtest['fare'].to_frame())

from sklearn.tree import plot_tree
plot_tree(fare_discretizer)
plt.show()

#%%
# New model, using age groups (as predicted by decision tree)
new_model = LogisticRegression(max_iter=500, n_jobs=-1)
new_model.fit(xtrain, ytrain)
print(confusion_matrix(ytest, new_model.predict(xtest)))

# Performance seems to be comparable for this simple example.