# Getting Started
## Basics
### Misc python info
- everything in Python is a python object
- if functions are attached to an object, they are called methods


### Values and argument passing
```python
a = [1,2,3]
b = a
a.append(4)
print(b) # [1,2,3,4]
```


### Typing in python
- `isinstance()` and `isiterable()` are useful functions...
```python
if not isinstance(x, list) and isiterable(x):
    x = list(x)
```
- "mutable" <=> object or values it contains can be modified (like lists, dicts, etc.)
    - strings and tuples are immutable
- "simple" types are called "scalar types"
    - `int, float, None, str, bool, ...`

### Lists in python
- list inserts are computationally expensive compared to append
- using `in` keyword is *slower* for lists than it is for dicts and sets
- `list1.extend(list2)` is faster than `list1 + list2` as the former extends `list1` and the latter one copies all elements to a new list


### Pythonic code snippets
#### Ternary expressions
```python
x = VALUE if CONDITION else VALUE
```
#### `*`-Operator
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