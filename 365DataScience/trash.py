#%%
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%%
x = np.arange(0, 70, 0.01)
np.array()
y = 0.01*(x-35)**2+10

#%%
sns.set(style='ticks', font='CMU Sans Serif', font_scale=1.2)
plt.plot(x, y, color='#00305e')
plt.ylim (0,30)
plt.yticks([8, 25], labels=['niedrig', 'hoch'])
plt.xticks([15, 25, 35, 45, 55])
plt.vlines(x=35, ymin=0, ymax=40, linestyle='--', color='0.8')
plt.xlabel("Alter in Jahren", size=14)
plt.ylabel("Cortisollevel", size=14)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
#plt.title("Abbildung 1")
plt.tight_layout()
#plt.show()
plt.savefig('/Users/moritz/Desktop/neelefig.pdf')


#%%
plt.plot(x, y)
plt.show()
plt.yl
