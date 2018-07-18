class OrthogonalGTPatterns:
    """
    Gelfand-Tsetlin patterns in bijection with irreducible representations of 
    the special orthogonal group. 

    Args:
    _row (list): top row of GT pattern
    _n (int): largest entry
    _d (int): depth (# of rows)
    _k (int): width (of top row)
    _strict (bool): strictness along rows

    """


    def __init__(self, top_row=[], strict=False, tab_rules=0):
        # precondition check
        if top_row is not None:
            top_row = tuple(top_row)
        if strict and any(top_row[i] <= top_row[i+1] for i in range(len(top_row)-1)):
            raise ValueError("The top row must be strictly decreasing")

        tableaux = ["Sundaram", "Koike-Terada", "Proctor"]
        self._type = tableaux[tab_rules]
        self._row = top_row
        self._n = len(top_row)
        self._strict = strict
        self._k = top_row[0]
        if self._type == "Sundaram":
            self._d = 2 * len(top_row) - 1
        elif self._type == "Koike-Terada":
            self._d = 3 * len(top_row)


    def __iter__(self):
        """ Returns an iterator that lists all the patterns with specified top row
        """

        # When top row is trivial
        if self._n == 0:
            return []
        # Setup the first row
        iters = [None]*self._d
        ret = [None]*self._d
        ret[0] = list(self._row)
        min_pos = 1
        row_index = 0
        iters[1] = self._row_iter(ret[0], row_index)
        row_index += 1
        pos = 1
        while pos >= min_pos:
            try:
                row_index = pos
                ret[pos] = next(iters[pos])
                pos += 1
                # If we've reached bottom row, yield and backstep
                if pos == self._d:
                    yield ret[:]
                    pos -= 1
                    continue
                iters[pos] = self._row_iter(ret[pos-1],row_index)
            except StopIteration:
                pos -= 1
                row_index += 1


    def _row_iter(self, upper_row, row_index):
        """
        Helper iterator for any row with a row above it.
        Odd row_index denotes that the size of the next row remains the same.
        """
        if self._type == "Sundaram":
            row = [x-1 for x in upper_row[1:]]
            row_len = len(row)
            pos = 0
            while pos >= 0:
                if pos == row_len:
                    if row_index % 2 == 0:
                        if (row_index == 0 and any(row[k] <= upper_row[k]-2 for k in range(len(row))))\
                            or row[-1] == 0:
                            pos -= 1
                            continue
                        yield row[:]

                    else:
                        for i in range(0, upper_row[pos]+1):
                            if self._strict and pos > 0 and i == row[pos-1]:
                                continue
                            ext_row = row + [i]
                            yield ext_row
                    pos -= 1
                    continue
                # If it would create an invalid entry, backstep
                if ( pos > 0 and (row[pos] >= row[pos-1] \
                        or (self._strict and row[pos] == row[pos-1]-1)))  \
                        or row[pos] >= upper_row[pos] \
                        or (self._k is not None and row[pos] >= self._k):
                    row[pos] = upper_row[pos+1] - 1
                    pos -= 1
                    continue
                row[pos] += 1
                pos += 1

        elif self._type == "Koike-Terada":
            if row_index % 3 == 2:
                yield upper_row[:-1]
            else:
                row = [x-1 for x in upper_row[1:]]
                row_len = len(row)
                pos = 0
                while pos >= 0:
                    if pos == row_len:
                        for i in range(0, upper_row[pos]+1):
                            if self._strict and pos > 0 and i == row[pos-1]:
                                continue
                            elif row_index % 3 == 1 and i not in [1,0]:
                                continue 
                            ext_row = row + [i]
                            yield ext_row
                        pos -= 1
                        continue

                    # If it would create an invalid entry, backstep
                    if ( pos > 0 and (row[pos] >= row[pos-1] \
                            or (self._strict and row[pos] == row[pos-1]-1)))  \
                            or row[pos] >= upper_row[pos] \
                            or (self._k is not None and row[pos] >= self._k):
                        row[pos] = upper_row[pos+1] - 1
                        pos -= 1
                        continue
                    row[pos] += 1
                    pos += 1




"""
KT = OrthogonalGTPatterns([2,1], True, 1)
for k in KT:
    print(k)
print('\n', len(list(KT)))


GT1 = OrthogonalGTPatterns([3,2,1],True)
GT2 = OrthogonalGTPatterns([2,1,0],True)
GT3 = OrthogonalGTPatterns([2,1],True)
gts1 = [gt for gt in GT1]
gts2 = [gt for gt in GT2]
gts3 = [gt for gt in GT3]
print(len(gts1), len(gts2), len(gts3))


GT22 = OrthogonalGTPatterns([2,1,0])
for k in GT22:
    print(k)

"""
