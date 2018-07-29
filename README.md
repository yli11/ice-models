# Requirements

Python3, SymPy.

# Usage

### Calculating the Partition Function

In command line, enter:

```
$ python3 main.py 3 1 0
# of patterns: 42
... (result omitted here because it's too long)
```

The script outputs a partition function, $\mathcal Z(\lambda)$, that is the product of a deformation of the Weyl denominator and a generalized character of a highest weight representation, by summing over our ice models corresponding to strict GT patterns with the given top row `3 1 0` .

One can use `-f` to get the factored partition function: 

```
$ python3 main.py 3 1 0 -f
# of patterns: 42
(t*z0 + 1)*(t*z0 + z1)*(t*z1 + 1)*(t*z0*z1 + 1)*(z0**2*z1 + z0*z1**2 + z0*z1 + z0 + z1)/(z0**3*z1**3)
```

Factoring the result takes some time, especially for large GT patterns.

Alternatively, it is possible to index the deformation parameter `t` by row with the `-i` flag:

_Note_: This formulation is not fully solved. The sum of weights does not give a deformed character formula.

```
$ python3 main.py 3 1 0 -i -f
# of patterns: 42
(t0*z0**2 + 1)*(t1*z1**2 + 1)*(t1**2*z0**4*z1**2 + t1**2*z0**3*z1**3 + t1**2*z0**3*z1**2 + t1**2*z0**3*z1 + t1**2*z0**2*z1**2 + t1**2*z0*z1**3 + t1**2*z0*z1**2 + t1**2*z0*z1 + t1**2*z1**2 + t1*z0**3*z1**3 + t1*z0**3*z1 + t1*z0**2*z1**4 + t1*z0**2*z1**3 + 2*t1*z0**2*z1**2 + t1*z0**2*z1 + t1*z0**2 + t1*z0*z1**3 + t1*z0*z1 + z0**2*z1**2)/(z0**2*z1**2)
```

#### Ice Model for Koike-Terada Tableau

For calculations based on the Koike-Terada tableau instead of the Sundaram tableau, use the `--KT` flag.

### Visualizing An Ice Model

For testing a single GT pattern, use (`-a` for U-turn boundaries on the right side):

```
$ python3 testIce.py -a
```

then enter the entire pattern line by line. Hit `return` one more time when done.

The script outputs a visualization of the ice model and a tally of vertex types by row.

### Visualizing (Shifted) Tableaux

To see the shifted tableaux corresponding to GT patterns of a given top row, use:

```
$ python3 tableau.py
```
# References

* Brubaker, B., Bump, D., & Friedberg, S. (2011). Schur Polynomials and The Yang-Baxter Equation. *Communications in Mathematical Physics*, *308*(2), 281–301.
* Brubaker, B., & Schultz, A. (2015). The six-vertex model and deformations of the Weyl character formula. *Journal of Algebraic Combinatorics*, *42*(4), 917–958.
* Gray, N. (2017). *Metaplectic Ice for Cartan Type C*.
* Hamel, A. M., & King, R. C. (2002). Symplectic Shifted Tableaux and Deformations of Weyl’s Denominator Formula for sp(2n). *Journal of Algebraic Combinatorics*, *16*(3), 269–300
* Koike, K., & Terada, I. (1990). Young diagrammatic methods for the restriction of representations of complex classical Lie groups to reductive subgroups of maximal rank. *Advances in Mathematics*, *79*(1), 104–135.
* Sundaram, S. (1990). Orthogonal tableaux and an insertion algorithm for SO(2n + 1). *Journal of Combinatorial Theory*, Series A, 53(2), 239-256.

