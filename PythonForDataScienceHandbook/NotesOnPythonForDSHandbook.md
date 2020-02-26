# iPython Introduction
## iPython Magic Commands
- prefixed by a '%' character (**line magic**) or '%%' (**cell magic**)
- `%run` runs external code (function are available in namespace afterwards)
- `%time` for simple runtime or `%%timeit` for multiple executions
- to suppress output, add `;` at the end of the line
- shell commands can be executed when preceeded by an `!`
## Other Magic Commands
### Available line magics:
```python
%alias  %alias_magic  %autoawait  %autocall  %automagic  %autosave  %bookmark  %cat  %cd  %clear  %colors  %conda  %config  %connect_info  %cp  %debug  %dhist  %dirs  %doctest_mode  %ed  %edit  %env  %gui  %hist  %history  %killbgscripts  %ldir  %less  %lf  %lk  %ll  %load  %load_ext  %loadpy  %logoff  %logon  %logstart  %logstate  %logstop  %ls  %lsmagic  %lx  %macro  %magic  %man  %matplotlib  %mkdir  %more  %mv  %notebook  %page  %pastebin  %pdb  %pdef  %pdoc  %pfile  %pinfo  %pinfo2  %pip  %popd  %pprint  %precision  %prun  %psearch  %psource  %pushd  %pwd  %pycat  %pylab  %qtconsole  %quickref  %recall  %rehashx  %reload_ext  %rep  %rerun  %reset  %reset_selective  %rm  %rmdir  %run  %save  %sc  %set_env  %store  %sx  %system  %tb  %time  %timeit  %unalias  %unload_ext  %who  %who_ls  %whos  %xdel  %xmode
```

### Available cell magics:
```python
%%!  %%HTML  %%SVG  %%bash  %%capture  %%debug  %%file  %%html  %%javascript  %%js  %%latex  %%markdown  %%perl  %%prun  %%pypy  %%python  %%python2  %%python3  %%ruby  %%script  %%sh  %%svg  %%sx  %%system  %%time  %%timeit  %%writefile
```

# Introduction to Numpy
## Python vs. Numpy
- python datatypes (like an int) are just cleverly disguised C-datatypes with some overhead
- numpys fixed datatype arrays save overhead

## Numpy Arrays
### Attributes
```python
a = np.array([[1,2,5], [10, 20, 50]])
print(a.ndim) # 2
print(a.size) # 6
print(a.shape) # (2, 3)
```
### Slicing
- works just like stock python (index, negative index, etc.)
- multiple dimensions can be accessed via index-tuple: `print(a[0, 2])`
- Example: Reverse in every dimension
```python
arr = np.array([[1,2,3],
                [4,5,6]])
arr[::-1, ::-1]
# array([[6, 5, 4],
#        [3, 2, 1]])
```
- Slicing returns view, `.copy()` creates real copy

### UFuncs
- `np.multiply.reduce(x)` for reducing array
- `np.multiply.accumulate(x)` for storing intermediate steps of reduction
- for each function (e.g. `np.mean()`) numpy provides an NaN-Safe version: `np.nanmean()``
- Broadcasting enables calculation between not equally-sized arrays (like scalar numerical operations)

### Comparison, Masks, Boolean Logic
- boolean arrays can be used as mask
- one can also check if there are any/only `True` values: `.any()` or `.all()`
- Boolean operators on arrays **MUST** be the python **bitwise** operators:
    - AND: `&`
    - OR: `|`
    - NOT: `~`
    - XOR: `^`

### Other Numpy Array Stuff
- *Structured* arrays and *Record* arrays can store multiple data types
- Record arrays allow column access via an attribute, not only via dictionary key

# Pandas
## Basics
- Pandas Series are generalized NumPy arrays: They have an explicit index
- Pandas Series can be thought of as *specialized dictionaries* but the single type makes them more efficient

## Data Frames
- Data Frames can also be thought of as 2-dimensional numpy arrays
    - rows are indexed by df.index
    - columns are indexed by df.columns
###  The Index
- index structure can be thought of as *immutable array* or *ordered set*
- when slicing with an explicit index, the final element is **included**
    - when slicing with an implicit index, **it is not.**
- `.loc`, `.iloc` and `.ix` are special *indexer attributes* to make clear which index (explicit = `.loc`, implicit = `.iloc`) you are using
- `.ix` is a hybrid of these two

### Multiindex
- Can be created by using tuples as dict-keys for creating a data frame
- can be stacked and unstacked
- `.reset_index()` turns index labels into columns
    - the opposite is `.set_index([cols])` which uses `cols` as indeces.

### Operations on Data Frames
- using ufuncs with pandas preserves/aligns index 

## Combining Datasets
- by default, *concatenation* takes place row-wise
- join is just a merge on index. Therefore, merge is more versatile

# Split-Apply-Combine
## Groupby
- using `.aggregate(...)` on a groupby object can aggregate by multiple functions or specific functions per column
=> Aggregate returns a reduce version of the data, `.transform(...)` returns the long version (same shape as input)
- pandas can group by dictionary:
```python
df.groupby({'A': 'vowel', 'B': 'consonant', 'C': 'consonant'}).sum()
```
|           | d1| d2|
|    ---    |---|---|
|consonant  | 12| 19|
|vowel      |  3|  8|

- pandas can group by any **function** that gets index as input and outputs group

## Pivot Tables
- in pivot tables, one can slica by cutted data:
```python
age = pd.cut(titanic['age'], [0, 18, 80])
titanic.pivot_table('survived', ['sex', age], 'class')
```
## Indicator Variables
- `.str.get_dummies(SPLITCHAR)` is also a valid getdummies call

# Time Series
## Datetime Objects
- available from different packages (vanilla python, numpy, pandas)

```python
import numpy as np 
date = np.array('2015-07-04', dtype=np.datetime64)
date + np.arange(12)
```

## Resampling
- can be done using `.asfreq()` or `.resample()``
    - `.asfrequ()` selects subset of datapoints
    - `.resample()` aggregates multiple data points

# Visualizing with Matplotlib