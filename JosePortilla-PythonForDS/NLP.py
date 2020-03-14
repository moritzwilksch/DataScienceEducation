# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%%
df = pd.read_csv("SMSSpamCollection", sep="\t", header=None, names=["label", "message"])
df.head()

# %%
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

PORTER_STEMMER = PorterStemmer()
ENG_STOPWORDS = stopwords.words("english")

def remove_punct(msgs):
    """ removes punctuation from a text_column in a df and converts it to lower case."""
    msgs = msgs.apply(lambda txt: txt.translate(str.maketrans("", "", string.punctuation)).lower())
    return msgs

def remove_stopwords(msgs):
    msgs = msgs.apply(lambda l: " ".join([word for word in l.split() if word not in ENG_STOPWORDS]))
    return msgs

def stem_words_porter(msgs):
    msgs = msgs.apply(lambda l: " ".join([PORTER_STEMMER.stem(word) for word in l.split()]))
    return msgs

def tokenize_words(msgs):
    msgs.apply(word_tokenize)
    return msgs
# %%
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split

TXTCOL = "message"

preprocessing_pl = Pipeline([
    ("Remove Punctuation", FunctionTransformer(remove_punct)),
    ("Remove Stopwords", FunctionTransformer(remove_stopwords)),
    ("Porter Stemmer", FunctionTransformer(stem_words_porter)),
])

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

conversion_pl = Pipeline([
    ("Count vectorize", CountVectorizer()),
    ("TFIDF", TfidfTransformer()),
])


# %%
xtrain, xtest, ytrain, ytest = train_test_split(df["message"], df.label, random_state=1234)


xtrain = conversion_pl.fit_transform(preprocessing_pl.fit_transform(xtrain))
xtest = conversion_pl.transform(preprocessing_pl.transform(xtest))

def single_str(msg):
    s = pd.Series(msg)
    return conversion_pl.transform(preprocessing_pl.transform(s))

# %%
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

naive_bayes = MultinomialNB()
naive_bayes.fit(xtrain, ytrain)
preds = naive_bayes.predict(xtest)
print("=== BASELINE: NAIVE BAYES ===\n")
print(classification_report(ytest, preds))

# %%
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()
lr.fit(xtrain, ytrain)
preds = lr.predict(xtest)
print("=== LOGISTIC REGRESSION ===\n")
print(classification_report(ytest, preds))

# %%
import keras

nn = keras.Sequential([
    keras.layers.Dense(units=10, input_dim=6893, activation="sigmoid"),
    keras.layers.Dense(units=1, activation="sigmoid")
])

nn.compile("nadam", "binary_crossentropy")
history = nn.fit(xtrain, ytrain.map({"ham":0, "spam":1}), validation_data=(xtest, ytest.map({"ham":0, "spam":1})), epochs=50, use_multiprocessing=True,batch_size=128)

# %%
plt.plot(history.history["val_loss"], label="test")
plt.plot(history.history["loss"], label="train")
plt.legend()

print("=== SHALLOW NEURAL NET ===\n")
preds = nn.predict_classes(xtest)
print(classification_report(ytest.map({"ham":0, "spam":1}), preds))