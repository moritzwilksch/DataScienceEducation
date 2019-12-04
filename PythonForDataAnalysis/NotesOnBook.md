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