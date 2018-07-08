from testIce import *
from generateGT import *
import sys

class Tableau:
    """
    Author: Johnny Gao
    A tableau represents a tableaux with certain entries
    arg: a GT pattern
    type: A or B. This determines the letters used. One can also determine its own letters
    shifted: if the tableau is shifted
    """

    def __init__(self, GT, type='B', shifted = False):
        self.shape = GT[0]
        self.size = len(GT)
        self.shifted = shifted

        self.tableau = [[] for x in range(len(self.shape))]
        for letter in range(1, self.size+1):
            ishape = GT[self.size-letter]
            for row in range(len(ishape)):
                aim = ishape[row]
                current = len(self.tableau[row])
                if current > aim:
                    raise ValueError("The GT patter shape must be weakly increasing")
                self.tableau[row] += [letter]*(aim-current)
        if self.shifted:
            for i in range(len(self.shape)):
                self.tableau[i] = ['.']*i + self.tableau[i]

        self.dict = {'.': '.'} # record the shifted entries
        if type=='A':
            for i in range(1, self.size+1):
                self.dict[i] = str(i)
        elif type=='B':
            for i in range(1, int(self.size/2) + 1):
                self.dict[2 * i - 1] = str(i)
                self.dict[2 * i] = self.overline(str(i))
            self.dict[self.size] = str(0)
        else:
            raise ValueError("Parameter 'type' has to be 'A' or 'B'")

    def overline(self, string):
        return ''.join(c+u'\u0305' for c in string)

    def __str__(self):
        string = ""
        for row in self.tableau:
            string +=' '.join(self.dict[entry] for entry in row) + '\n'
        return string


if __name__ == "__main__":
    text = input("Please enter the top row of the GT pattern:")
    top_row = [int(x) for x in text.split()]
    GT = OrthogonalGTPatterns(top_row, True)
    # print(len(list(GT)))
    for gt in GT:
        tableau = Tableau(gt, type='B', shifted=True)
        print(tableau)
