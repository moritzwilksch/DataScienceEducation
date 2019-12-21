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
