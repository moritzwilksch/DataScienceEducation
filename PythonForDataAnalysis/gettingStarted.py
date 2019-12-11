# %%
import pandas as pd
import requests
url = 'https://api.github.com/repos/pandas-dev/pandas/issues'
resp = requests.get(url)
data = pd.DataFrame(resp.json())

# %%
pd.read_json(url)


# %%
import seaborn as sns
df = sns.load_dataset("titanic")
df.groupby(["pclass", "sex"])["age"].mean()
df["age"] = df["age"].fillna(df.groupby(["pclass", "sex"])["age"].transform("mean"))


# %%
