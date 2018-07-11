

## Requirements

python3, SymPy.

## Usage

### Calculating Character Formula

In command line, enter:

```
$ python3 main.py
```

You will be prompted to enter the top row of the GT pattern. Separate entries by a whitespace. Hit `enter` again when done.
The script outputs a polynomial (deformed character formula) based on all legal GT patterns with the given top row and their corresponding ice models and Boltzmann weights.

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