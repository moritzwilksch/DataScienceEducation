# %% [markdown]
# # Imports

# %%
import matplotlib.pyplot as plt
import numpy as np
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
df["age"] = df["age"].fillna(df.groupby(["pclass", "sex"])[
                             "age"].transform("mean"))

# %% [markdown]
# # String Operations
# %%
s = "Doe, John"
words = s.split(",")  # ["Doe", " John"]
words = [w.strip() for w in words]
name = "::".join(words)  # 'Doe::John'
name.index("J")  # 5
name.find("XX")  # -1
name.count(":")  # 2
name.replace("::", "<br>")  # 'Doe<br>John'

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
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)
ax1 = sns.distplot(df.total_bill)
plt.show()

# Better:
fig, ax = plt.subplots(2, 2)
sns.distplot(df.total_bill, ax=ax[0, 0])
sns.distplot(df.tip, ax=ax[0, 1])


ax[0, 0].set_xticks([20, 40])
ax[0, 0].set_xticklabels(["zwanzig", "vierzig"])
plt.show()

# %% [markdown]
# ## Example: Subplots and Styling
# %%
HIST_STYLE = {"alpha": 0.2}

sns.set_palette("bright")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
sns.distplot(df.tip, ax=ax[0], hist_kws=HIST_STYLE)
tips = np.array([df.tip.sample(50, replace=True).mean() for i in range(1000)])
perfect = np.random.normal(loc=tips.mean(), scale=tips.std(), size=1000)
sns.distplot(tips, ax=ax[1], hist_kws=HIST_STYLE)
ax[0].set_title("Distribution of tip", size=16)
ax[1].set_title("Distribution of mean of tip\n(sample size = 50)", size=16)
ax[0].set_yticks([])
ax[0].set_xlabel("Tip in USD", size=16)
ax[1].set_xlabel("Sampled means of in USD", size=16)
ax[1].set_yticks([])
sns.distplot(perfect, ax=ax[1], hist=False,
             label="Normal Distribution with same mean & std")
plt.show()

# %% [markdown]
# ## Annotating Plots
# %%
fig, ax = plt.subplots(2, 2)
sns.distplot(df.total_bill, ax=ax[0, 0])
sns.distplot(df.tip, ax=ax[0, 1])
ax[0, 0].text(20, 0.04, "Hello world!")

# %% [markdown]
# # Grouping and Aggregating
# %%
df.groupby("sex").agg(np.var)

