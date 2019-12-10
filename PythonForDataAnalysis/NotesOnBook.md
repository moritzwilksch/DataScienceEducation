
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
- Generators return results laizly as they are needed (use `yield` instead of `return` inside function)
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


