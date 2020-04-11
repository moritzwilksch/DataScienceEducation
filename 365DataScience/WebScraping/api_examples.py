#%%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

#%%
base_url = 'https://api.exchangeratesapi.io/latest'
response = requests.get(base_url)
print(f"Response: ok={response.ok}, status_code={response.status_code}")
print(response.text)  # String version
print(response.content)  # byte version
print(response.json()) # JSON version (converted to python dict)

#%%
type(response.json())  # dict

#%%
print(json.dumps(response.json(), indent=2))

#%%
# Specifying Parameters
param_url = base_url + "?symbols=USD,GBP"
param_response = requests.get(param_url)
print(param_response.json())

# Different base currency
param_url = base_url + "?symbols=GBP&base=USD"
param_response = requests.get(param_url)
print(param_response.json())
data = param_response.json()
print(data['rates']['GBP'])

#%%
# Different Endpoint
base_url = 'https://api.exchangeratesapi.io'
date_url = base_url + "/2019-05-12"

date_response = requests.get(date_url)
print(date_response.json())

#%%
# Time Period
period_url = base_url + "/history?start_at=2018-01-01&end_at=2019-01-01&symbols=USD,GBP"
period_response = requests.get(period_url)
data = period_response.json()

#%%
# Using requests to pass params (preferred)
r = requests.get(base_url + "/history", params={'start_at': '2018-01-01', 'end_at': '2019-01-01', 'symbols': 'USD,'
                                                                                                              'GBP'})
# requests.get can take a limit parameter
print(r.json())

#%%
# Pagination
base_url = 'https://jobs.github.com/positions.json'
r = requests.get(base_url)
print(len(r.json()))

# Second request: parameter page=2
r = requests.get(base_url, params={'page':2})
print(len(r.json()))