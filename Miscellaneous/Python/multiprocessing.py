# %%
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize
import pandas as pd

df = pd.Series(twitter_samples.strings('positive_tweets.json'))

# %%
import multiprocessing as mp
import time


def prep(tweet):
    return " ".join([word.lower() for word in word_tokenize(tweet)])


# %%
# 0.9815 seconds
starttime = time.time()
[prep(tweet) for tweet in df]
endtime = time.time()
print(endtime - starttime)

# %%
# 0.3350 seconds
starttime = time.time()
with mp.Pool(mp.cpu_count()) as p:
    p.map(prep, df)
endtime = time.time()
print(endtime - starttime)
