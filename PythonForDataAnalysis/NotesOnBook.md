
# Python Basics
## Misc Python Info
- everything in Python is a python object
- if functions are attached to an object, they are called methods


## Values and Argument Passing
```python
a = [1,2,3]
b = a
a.append(4)
print(b) # [1,2,3,4]
```


## Typing in Python
- `isinstance()` and `isiterable()` are useful functions...
```python
if not isinstance(x, list) and isiterable(x):
    x = list(x)
```
- "mutable" <=> object or values it contains can be modified (like lists, dicts, etc.)
    - strings and tuples are immutable
- "simple" types are called "scalar types"
    - `int, float, None, str, bool, ...`

## Lists in Python
- list inserts are computationally expensive compared to append
- using `in` keyword is *slower* for lists than it is for dicts and sets
- `list1.extend(list2)` is faster than `list1 + list2` as the former extends `list1` and the latter one copies all elements to a new list


# Pythonic Code Snippets
## Ternary Expressions
```python
x = VALUE if CONDITION else VALUE
```
## `*`-Operator
- in function header: `def myFun(*a, **kw):` `a` collects all positional arguments in one tuple and `kw` collects all keyword arguments in one dict
- in function call: `*` _unpacks_ a tuple into positional arguments for the function and `**` unpacks a dictionary into keyword arguments
```python
# In function header...
def functionA(*a, **kw):
    print(a)
    print(kw)
functionA(1, 2, 3, 4, 5, 6, a=2, b=3, c=5)
# (1, 2, 3, 4, 5, 6)
# {'a': 2, 'c': 5, 'b': 3}

# ... and in function call
lis=[1, 2, 3, 4]
dic={'a': 10, 'b':20}
functionA(*lis, **dic)  # is similar to functionA(1, 2, 3, 4, a=10, b=20)
```

## Generator Object
- A generator is a concise way to create a new iterable
- Generators return results lazily as they are needed (use `yield` instead of `return` inside function)
```python
def squares(n):
    for i in range(n):
        yield i ** 2
gen = squares(15)
for x in gen:
    print(x)
```
# Error Handling in Python
## General Structure
```python
try:
    # Code
except:
    # Error handling
```
### Catching Specific Errors
```python
try:
    # Code
except ValueError, TypeError:
    # Error handling
```

# Numpy Basics
> Numpy operations are generally 10 to 100 times faster than their python equivalent!
## Numpy's USP: ndarray
- create array with `np.array(SEQUENCE)`
- `np.arrange()` is the numpy equivalent to the python `range()` function
- numpy datatypes are {int, float}x{8, 16, 32, 64}
- Be careful using `np.string_` datatype. It has a fixed length and might truncate values!
- Any arithmetic operations between equal-size arrays applies the operation element-wise (vectorization)
- Operation on slices of arrays will affect the original array, as slices are only views!
    - use `arr.copy()` to explicitly copy values
- slicing multidimensional arrays
```python
arr = np.array([[1,2,3],
                [4,5,6],
                [7,8,9]])
print(arr[:2, 1:])
# [[2 3]
# [5 6]]
```
- Python keywords `and` and `or` don't work with boolean indexing, use `&` and `|` respectively
- negate boolean indexing using `~EXPRESSION`
- "Fancy indexing": Using list of indexes to obtain elements at these indecies
> Fancy indexing always copies data, slicing DOES NOT!

## Universal Functions (ufuncs)
- fast (vectorized) element-wise execution of function
- **unary** functions: `np.sqrt(a), np.exp(a)``
- **binary** functions: `np.maximum(a,b)
- `.cumsum()` and `.cumprod` return array of intermediate steps
- `np.where(CONDITION, [VALUEifTRUE], [VALUEifFalse])`
```python
arr = np.array(range(10,20))
print(np.where(arr % 2 == 0, arr, -1))
#[10 -1 12 -1 14 -1 16 -1 18 -1]
```
- `np.save()` and `np.load()` can be used to save arrays to disk in raw binary format (.npy) 


# Getting Started with pandas
## Basics
- As with numpy arrays, indexed rows or columns are views on the df, so modifications will alter the original object

### The Index
- As opposed to numpy, the index of a Series or DataFrame can be labels, not only numbers
- The index stores axis names 
- Series can be interpreted as a dictionary-like key-value-mapping from index to data value
- pandas index objects are **immutable**!

## Essential Functionality
### Reindexing
- `df.reindex(...)` creates new object based on data from df that conforms to the provided index
- provided index can be index of rows or index of columns

### Indexing, Selection, Filtering
- As opposed to numpy indexing, one can use labels of the index for Filtering and Slicing
> **CAUTION:** Slicing with labels **includes** the endpoint!
- `.loc[...]` enables selection based on labels
- `.iloc[...]` enables selection based on integers

### Sorting
- `df.sort_index()` sorts by index (either rows or columns)
- `df.sort_values()` sorts by values

## Data Loading, Storage and File Formats
### Loading and Saving
- `pd.read_csv(...)` has over 50 possible parameters such as separator, header, null_values, ...
- Python has a standard library called `json` to import and export python objects as json
- pandas' `.read_json(...)` assumes that each object in the json-array is a row in th DataFrame
- HDF5-Format is especially suited for large datasets that don't fit into memory
- There are many python-SQL-drivers available, most of which return a list of tuples when executing a query
    - Column names must be provided manually when working with tuples
    - SLQAlchemy is a library that provides an abstract layer and can easily be used with DataFrames
### Interacting with web APIs
- use the python `requests`-package
```python
import pandas as pd
import requests
url = 'https://api.github.com/repos/pandas-dev/pandas/issues'
resp = requests.get(url)
data = pd.DataFrame(resp.json())
# ODER:
pd.read_json(url)
```

# Data Cleaning and Preparation
## Missing Data
Example of using fillna(...) with groupby:
```python
import seaborn as sns
df = sns.load_dataset("titanic")
# Show table of groups with mean of age:
df.groupby(["pclass", "sex"])["age"].mean()

# Fill NAs by group
df["age"] = df["age"].fillna(df.groupby(["pclass", "sex"])["age"].transform("mean"))
```
=> one needs to use `.transform("mean")` instead of `.mean()`, because transform returns the whole series of ages (891 in this case), not just shows the 6 groups.

## Data Transformation
### General and String Operations
- `.duplicated()` returns boolean array showing whether a row has been observed before (aka is duplicated)
- String methods can be applied to whole columns: `df["a"].str.lower()`
- `.map(DICT)` is a helpful tool for data transformation

### Renaming Axis Indexes
- like values, indexes can be alterd too, e.g. by using `df.index = df.index.map(FUNC)`
- To rename indexes inplace use `df.rename(DICT, inplace=True)`

### Numeric Transformations
- use `pd.cut(Series, ListOfBins)` to cut Series into bins
    - you can pass `labels=[...]` or use `.qcut(...)` to cut into quartiles

### Detecting and Filtering Outliers
- `np.sign(df)` produces -1 for negative values and 1 for positive values (useful for z-values)
- `df.sample(n=...` takes random sample **without replacement**
    - for replacements pass `replace=True` as additional parameter

### Dummy Variables
- `df1.join(df2)` can combine two DataFrames
```python
catcols = df.select_dtypes("category").columns
dummies = pd.get_dummies(df[catcols])
df.join(dummies)
```

### String Operations
```python
s = "Doe, John"
words = s.split(",") # ["Doe", " John"]
words = [w.strip() for w in words]
name = "::".join(words) # 'Doe::John'
name.index("J") # 5
name.find("XX") # -1
name.count(":") # 2
name.replace("::", "<br>") #'Doe<br>John'
```
=> `.index(...)` throws exception when element is not found, `.find(...)` returns `-1`

### Regular Expressions
- import regex module `import re`
- if used multiple times, manually compile the regular expression to save CPU time: `re.compile("REGEX")`
- regex objects have a `.findall(SOURCE)` method
- `re.match(...)` can contain groups (such as name, domain, and TLD of an email address)
- pandas string methods are available via `SERIES.str.METHOD`
- p217/218???
