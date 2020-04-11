#%% md

# Bootstrapping Credible Intervals

#%%

import seaborn as sns
sns.set_style('ticks')
import matplotlib.pyplot as plt
import numpy as np

df = sns.load_dataset('tips')

"""group_a = df.query("day=='Thur'")['tip']
group_b = df.query("day=='Sun'")['tip']
"""

group_a = df.query("time=='Lunch'")['tip']
group_b = df.query("time=='Dinner'")['tip']

sns.distplot(group_a)
sns.distplot(group_b)
plt.title("Distribution of Tips.")
plt.show()

#%%

# Number of Bootstraps doesn't really affect Credible Interval, ONLY ITS CONVERGENCE!
n_bootstraps = 1000

# Each sample drawn should be as big as the original sample (len(group_a))!!!!
# Drawing larger samples would narrow the resulting Credible Interval  thereby simulating
# what CI would result if the ORIGINAL SAMPLE HAD BEEN BIGGER TO BEGIN WITH!!!!!
# This can be used for minimum sample size estimation.
mean_a = np.mean(np.random.choice(group_a, (n_bootstraps, len(group_a))), axis=1)
mean_b = np.mean(np.random.choice(group_b, (n_bootstraps, len(group_b))), axis=1)
# Bootstraped sample size HEAVILY AFFECTS CI (variance of the mean of 10M values sampled from 68
# is waaaaaaay lower than variance of the mean of 68 samples sampled from 68

#%% md

## Explanation
Each sample drawn should be ***as big as the original sample*** (`len(group_a)`)!!!!
Drawing larger samples would narrow the resulting Credible Interval  thereby simulating
what CI would result if the ***ORIGINAL SAMPLE HAD BEEN BIGGER TO BEGIN WITH***!!!!!
This can be used for minimum sample size estimation. However, sampling a larger number than items in the original sample would lead to wrong results (CI is much narrower)



#%%

sns.distplot(mean_a)
sns.distplot(mean_b)
plt.title(f"Mean Tip. {n_bootstraps} Bootstraps.")
plt.show()

#%%

diff_means = mean_b - mean_a
lower, upper = np.round(np.percentile(diff_means, (2.5, 97.5)), 4)
sns.distplot(diff_means, kde=False)
plt.title(fr"Difference in Means. 95CI: {(lower, upper)}")
plt.axvline(lower, color='0.5')
plt.axvline(upper, color='0.5')
plt.show()

#%% md

#### Sampling n=68=`len(a)` items for b=1000000 times, CI converges to (0.015, 0.72)
#### Sampling n=1000000 (way too many) items for b=10000 times, CI FALSELY NARROWS to (0.36, 0.39)

#%%
a_exp = np.asarray([19.17, 3.94, 5.9]).reshape((-1,1))
b_exp = np.asarray([19.83, 4.06, 6.1]).reshape((-1,1))

def get_ad(n_iter = 1000):
    a = np.random.choice([1]*39+[2]*8+[3]*12, (n_iter, 29))
    a_vc = np.asarray(
        [np.count_nonzero(a==1, axis=1),
        np.count_nonzero(a==2, axis=1),
        np.count_nonzero(a==3, axis=1),]
    )
    b = np.random.choice([1]*39+[2]*8+[3]*12, (n_iter, 30))
    b_vc = np.asarray(
        [np.count_nonzero(b==1, axis=1),
        np.count_nonzero(b==2, axis=1),
        np.count_nonzero(b==3, axis=1),]
    )

    a_ad = np.sum(np.abs(a_vc - a_exp), axis=0)
    b_ad = np.sum(np.abs(b_vc - b_exp), axis=0)

    return a_ad + b_ad





