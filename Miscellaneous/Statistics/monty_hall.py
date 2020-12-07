#%%
import numpy as np

#%%
def generate(n=1000, stay=True):
    results = []
    for i in range(n):
        prizes = np.random.randint(0, 3)
        prizes = np.eye(3)[prizes]
        first_choice = np.random.randint(0, 3)
        if prizes[first_choice] == 1:
            mod_choices = np.setdiff1d([0, 1, 2], first_choice, assume_unique=True)
        else:
            mod_choices = np.setdiff1d([0, 1, 2], [first_choice, np.where(prizes==1)[0].item()])
        mod_choice = np.random.choice(mod_choices)
        if stay:
            final_choice = first_choice
        else:
            final_choice = np.setdiff1d([0, 1, 2], [first_choice, mod_choice])
        
        results.append(prizes[final_choice].item())
    return results

#%%
# ca. 900 ms on my machine
n = 5000
stay = generate(n, True)
change = generate(n, False)

#%%
import matplotlib.pyplot as plt
import seaborn as sns

stay_pct = np.cumsum(stay)/np.arange(n)
change_pct = np.cumsum(change)/np.arange(n)

burn_in = 5
sns.lineplot(y=stay_pct[burn_in:], x=np.arange(burn_in, n), label="Stay with first choice")
sns.lineplot(y=change_pct[burn_in:], x=np.arange(burn_in, n), label="Switch choice")
plt.title("% of games won");

#%%
#############################################
# NOW, LETS USE NUMBA TO MAKE THINGS FAST! ##
#############################################
from numba import jit

@jit(nopython=True)
def generate_numba(n=1000, stay=True):
    results = [np.int(x) for x in range(0)]  # Hacky, but needed for nubma type inference
    for _ in range(n):
        prize_at = np.random.randint(0, 3)
        first_choice = np.random.randint(0,3)
        if prize_at == first_choice:
            mod_choices = [0, 1, 2]
            mod_choices.remove(first_choice)
        else:
            mod_choices = [0, 1, 2]
            mod_choices.remove(first_choice)
            mod_choices.remove(prize_at)
        mod_choice = np.random.choice(np.array(mod_choices))

        if stay:
            final_choice = first_choice
        else:
            final_choice_aux = [0,1,2]  # Use aux variable, cuz numba-var "final_choice" needs to have ONE static type!
            final_choice_aux.remove(mod_choice)
            final_choice_aux.remove(first_choice)
            final_choice = final_choice_aux[0]
        results.append(int(final_choice == prize_at))
    return results

#%%
# ca. 9ms on my machine - after the first slow compilation run
n = 5000
stay = generate_numba(n, True)
change = generate_numba(n, False)


#%%
stay_pct = np.cumsum(stay)/np.arange(n)
change_pct = np.cumsum(change)/np.arange(n)

burn_in = 5
sns.lineplot(y=stay_pct[burn_in:], x=np.arange(burn_in, n), label="Stay with first choice")
sns.lineplot(y=change_pct[burn_in:], x=np.arange(burn_in, n), label="Switch choice")
plt.title("% of games won");
