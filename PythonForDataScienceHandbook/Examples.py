# %%
import numpy as np


# %% [markdown]
# # iPython Magic Commands
# ## Measuring Runtime
# %%
%time
print("hi")

# %%
%%timeit
print("hi")
# %%
%%html
<h1>Hi in HTML</h1>

# %% [markdown]
# ## Running Shell Commands
# %%
!pwd
# %% [markdown]

""" 
## Other Magic Commands
### Available line magics:
%alias  %alias_magic  %autoawait  %autocall  %automagic  %autosave  %bookmark  %cat  %cd  %clear  %colors  %conda  %config  %connect_info  %cp  %debug  %dhist  %dirs  %doctest_mode  %ed  %edit  %env  %gui  %hist  %history  %killbgscripts  %ldir  %less  %lf  %lk  %ll  %load  %load_ext  %loadpy  %logoff  %logon  %logstart  %logstate  %logstop  %ls  %lsmagic  %lx  %macro  %magic  %man  %matplotlib  %mkdir  %more  %mv  %notebook  %page  %pastebin  %pdb  %pdef  %pdoc  %pfile  %pinfo  %pinfo2  %pip  %popd  %pprint  %precision  %prun  %psearch  %psource  %pushd  %pwd  %pycat  %pylab  %qtconsole  %quickref  %recall  %rehashx  %reload_ext  %rep  %rerun  %reset  %reset_selective  %rm  %rmdir  %run  %save  %sc  %set_env  %store  %sx  %system  %tb  %time  %timeit  %unalias  %unload_ext  %who  %who_ls  %whos  %xdel  %xmode

### Available cell magics:
%%!  %%HTML  %%SVG  %%bash  %%capture  %%debug  %%file  %%html  %%javascript  %%js  %%latex  %%markdown  %%perl  %%prun  %%pypy  %%python  %%python2  %%python3  %%ruby  %%script  %%sh  %%svg  %%sx  %%system  %%time  %%timeit  %%writefile

"""


# %% [markdown]
# # Numpy
# ## Numpy Array Attributes

# %%
a = np.array([[1,2,5], [10, 20, 50]])
print(a.ndim)
print(a.size)
print(a.shape)
print(a[0, 2])

# %% [markdown]
# ## Slicing in all Dimensions

# %%
arr = np.array([[1,2,3],
                [4,5,6]])
arr[::-1, ::-1]

# %% [markdown]
# # Pandas
# %%
import pandas as pd
s = pd.Series([1,2,3])
