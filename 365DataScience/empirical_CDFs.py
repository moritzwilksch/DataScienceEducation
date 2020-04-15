# %%
# Requires Python 3.8
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style='ticks', font="CMU Sans Serif", font_scale=1.2)
# %%
df = sns.load_dataset('tips')

# %%
# density parameter used to show density instead of frequency on y-axis
plt.hist(df.tip, cumulative=True, histtype='step', density=True, color='b', lw=2, bins=len(df.tip))
plt.xlabel("Tip (USD)")
plt.ylabel("Empirical CDF")
plt.title("Empirical CDF for Tips ($)")
plt.show()

# %%

# Comparing 2 CDFs
plt.hist(data_slice := df.loc[df.day == 'Sun', 'tip'],
         cumulative=True,
         histtype='step',
         density=True, color='b',
         lw=2,
         bins=len(data_slice), label='Sundays'
         )

plt.hist(data_slice := df.loc[df.day == 'Sat', 'tip'],
         cumulative=True,
         histtype='step',
         density=True,
         color='r',
         lw=2,
         bins=len(data_slice), label='Saturdays'
         )
plt.xlabel("Tip (USD)")
plt.ylabel("Empirical CDF")
plt.title("Empirical CDF for Tips ($)")
plt.legend(loc=2)
plt.show()


