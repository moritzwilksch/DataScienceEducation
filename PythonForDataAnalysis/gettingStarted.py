# %%
import pandas as pd
import requests
url = 'https://api.github.com/repos/pandas-dev/pandas/issues'
resp = requests.get(url)
data = pd.DataFrame(resp.json())

# %%
pd.read_json(url)


# %%
