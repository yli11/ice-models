

## Requirements

Python3, SymPy.

## Usage

### Calculating Character Formula

In command line, enter:

```
$ python3 main.py 3 1 0
# of patterns: 42
(t*z0**2 + 1)*(t*z1**2 + 1)*(t**2*z0**4*z1**2 + t**2*z0**3*z1**3 + t**2*z0**3*z1**2 + t**2*z0**3*z1 + t**2*z0**2*z1**2 + t**2*z0*z1**3 + t**2*z0*z1**2 + t**2*z0*z1 + t**2*z1**2 + t*z0**3*z1**3 + t*z0**3*z1 + t*z0**2*z1**4 + t*z0**2*z1**3 + 2*t*z0**2*z1**2 + t*z0**2*z1 + t*z0**2 + t*z0*z1**3 + t*z0*z1 + z0**2*z1**2)/(z0**2*z1**2)
```

The script outputs a deformed character formula based on all ice models corresponding to legal GT patterns with the given top row `3 1 0` .



Alternatively, it is possible to index `t` in the deformation formula with the `-i` flag:

```
$ python3 main.py -i 3 1 0
# of patterns: 42
(t0*z0**2 + 1)*(t1*z1**2 + 1)*(t1**2*z0**4*z1**2 + t1**2*z0**3*z1**3 + t1**2*z0**3*z1**2 + t1**2*z0**3*z1 + t1**2*z0**2*z1**2 + t1**2*z0*z1**3 + t1**2*z0*z1**2 + t1**2*z0*z1 + t1**2*z1**2 + t1*z0**3*z1**3 + t1*z0**3*z1 + t1*z0**2*z1**4 + t1*z0**2*z1**3 + 2*t1*z0**2*z1**2 + t1*z0**2*z1 + t1*z0**2 + t1*z0*z1**3 + t1*z0*z1 + z0**2*z1**2)/(z0**2*z1**2)
```



### Visualizing An Ice Model

For testing a single GT pattern, use (`-a` for U-turn boundaries on the right side):

```
$ python3 testIce.py -a
```

then enter the entire pattern line-by-line.

The script outputs a visualization of the ice model and a tally of vertex types by row.

### Visualizing (Shifted) Tableaux

To see the shifted tableaux corresponding to GT patterns of a given top row, use:

```
$ python3 tableau.py
```