# %% [markdown]
# # Imports

# %%
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

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

# %% [markdown]
# # Matplotlib
# %%
df = sns.load_dataset("tips")


# %% [markdown]
# ## Figure and Axes
# %%
fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)
ax1 = sns.distplot(df.total_bill)
plt.show()

# Better:
fig, ax = plt.subplots(2,2)
sns.distplot(df.total_bill, ax=ax[0,0])
sns.distplot(df.tip, ax=ax[0,1])


ax[0,0].set_xticks([20, 40])
ax[0,0].set_xticklabels(["zwanzig", "vierzig"])
plt.show()


# %%


# %%
