# %% [markdown]
# # Imports

# %%
import pandas as pd
import requests
import seaborn as sns

# %% [markdown]
# # Requests from URL
# ## Fetching Data
# %%
url = 'https://api.github.com/repos/pandas-dev/pandas/issues'
resp = requests.get(url)

# %% [markdown]
# ## Handling the JSON format
# %%
data = pd.DataFrame(resp.json())
pd.read_json(url)

# %% [markdown]
# # Fill NA by group
# %%
df = sns.load_dataset("titanic")
df.groupby(["pclass", "sex"])["age"].mean()
df["age"] = df["age"].fillna(df.groupby(["pclass", "sex"])["age"].transform("mean"))

# %% [markdown]
# # String Operations
# %%
s = "Doe, John"
words = s.split(",") # ["Doe", " John"]
words = [w.strip() for w in words]
name = "::".join(words) # 'Doe::John'
name.index("J") # 5
name.find("XX") # -1
name.count(":") # 2
name.replace("::", "<br>") #'Doe<br>John'

# %% [markdown]
# # Regular Expressions
# %%
data.head()
ma = data["body"].str.findall(".*Code.*")
ma

# %% [markdown]
# # Merging and Joining
# %%
items = pd.DataFrame({
    "name": ["Rotwein", "Weisswein", "Suppe", "Kekse", "Rotwein", "asd"]
})

categories = pd.DataFrame({
    "name": ["Rotwein", "Weisswein", "Suppe", "Kekse"],
    "category": ["Wein", "Wein", "Essen", "Essen"]
})
m = pd.merge(items, categories, how="left")
m

# %%
