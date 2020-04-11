#%%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import lxml
#%%
r = requests.get('https://en.wikipedia.org/wiki/Music')
# lxml needs to be installed but is faster and better than the vanilla html.parser!
soup = BeautifulSoup(r.content, 'lxml')

#%%
links = soup.find_all('a')

#%%
print(links[2].attrs)
print(links[2]['href'])
# better:
print(links[2].get('href'))
