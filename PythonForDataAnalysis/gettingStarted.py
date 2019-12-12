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
df.info()


# %%
s = "Doe, John"
words = s.split(",") # ["Doe", " John"]
words = [w.strip() for w in words]
name = "::".join(words) # 'Doe::John'
name.index("J") # 5
name.find("XX") # -1
name.count(":") # 2
name.replace("::", "<br>") #'Doe<br>John'

# %%
data.head()

# %%
ma = data["body"].str.match("Code")

# %%