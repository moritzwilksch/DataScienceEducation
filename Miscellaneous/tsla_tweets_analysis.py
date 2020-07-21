# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# %%
raw = pd.read_csv('data/tsla_tweets.csv')

# %%
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from typing import List
import re
import string

sws = set(stopwords.words('english'))
to_remove = sws.union(string.punctuation)
stemmer = PorterStemmer()


def prepare(s: str) -> List[str]:
    s = re.sub(r'@\S+|https?://\S+', '', s)
    l = [stemmer.stem(word.strip()) for word in word_tokenize(s.lower()) if word not in to_remove]
    return l


# %%
tokenized_tweets = raw['tweet'].apply(prepare)

# %%
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()
cv.fit([" ".join(tweet) for tweet in tokenized_tweets])

# %%
df = raw[['date', 'tweet']]
performance = pd.Series([1, 0], index=pd.DatetimeIndex(["2020-05-14", "2020-05-13"]), name='return')
# %%
df['date'] = df['date'].astype('datetime64')
df_merge = pd.merge(df, performance, left_on='date', right_index=True)
# %%
df_merge.tail()
# %%
import keras
from keras.preprocessing.sequence import pad_sequences

# %%
X = cv.transform([" ".join(tweet) for tweet in df_merge['tweet']])
y = df_merge['return'].values
#%%
n_vocabs = len(cv.vocabulary_)

# %%
model = keras.Sequential([
    keras.layers.Dense(units=1000, input_dim=n_vocabs, activation='sigmoid'),
    keras.layers.Dense(units=1, activation='sigmoid')
])

model.compile('adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=1, batch_size=128)
# ACC = 72.7%

# %%
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

tk = Tokenizer(num_words=n_vocabs, lower=True, split=' ')
tk.fit_on_texts(df_merge['tweet'])
seqs = tk.texts_to_sequences(df_merge['tweet'])
Xemb = pad_sequences(seqs, maxlen=280)

xemb_train, xemb_test, ytrain, ytest = train_test_split(Xemb, y)
#%%
embedding = keras.Sequential([
    keras.layers.Embedding(input_dim=n_vocabs, output_dim=20, input_length=280),
    # keras.layers.AveragePooling1D(),
    keras.layers.Flatten(),
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1, activation='sigmoid')
])

#%%
embedding.compile('adam', loss='binary_crossentropy', metrics=['accuracy'])
embedding.fit(xemb_train, ytrain, validation_data=(xemb_test, ytest), epochs=10, batch_size=128)


# %%
hist = pd.DataFrame(embedding.history.history)
hist[['val_accuracy', 'accuracy']].plot()
plt.show()

#%%
erg = pd.DataFrame({'real': ytest, 'pred': embedding.predict_classes(xemb_test).reshape(-1)})

#%%
from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(erg['real'], erg['pred']))
print()
print(classification_report(erg['real'], erg['pred']))

#%%
def predict_on_new(text: str) -> int:
    tokenized = tk.texts_to_sequences([text])
    Xi = pad_sequences(tokenized, maxlen=280)
    return embedding.predict_classes([Xi])[0,0]

#%%
new = pd.read_csv("/Users/Moritz/PycharmProjects/TestPyCharm/today_twint.csv")
todaypreds = new['tweet'].apply(predict_on_new)

#%%
backtest_raw = raw.query("date == '2020-05-14'")['tweet']
backtest = backtest_raw.apply(predict_on_new)

#%%
senti = np.cumsum(todaypreds)/(np.arange(len(todaypreds))+1)
sns.lineplot(x=senti.index, y=senti)
plt.show()

#%%
