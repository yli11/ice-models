from generateGT import *
from testIce import *
import sys



def apply_weight(poly, weights):
    """ Plug in weights and check polynomial sum
    """
    return


def to_latex(count):
    """ Return a list of factors and the product of all terms as LaTex-format strings
        Directions of inward arrows: NE, SW, NW, SE, NS, EW
    """
    terms = []
    var_names = {(-1,-1,1,1):'NE', (1,1,-1,-1):'SW', (-1,1,1,-1):'NW', (1,-1,-1,1):'SW', (-1,1,-1,1):'NS', (1,-1,1,-1):'EW'}
    for i, row in enumerate(count):
        reduced = {x:y for x,y in row.items() if y!=0}
        for key, val in reduced.items():
            terms.append(var_names[key]+"_"+str(i)+"^"+str(val)+' ')
    latex = ''.join(terms)
    return terms, latex



def sum(list_of_rows):
    """ Given a list of top row partitions, return the sum over all of them
    """
    return

if __name__ == "__main__":
    text = input("Please enter the top row of the GT pattern:")
    top_row = [int(x) for x in text.split()]
    GT = OrthogonalGTPatterns(top_row,True)
    summands = []
    latex_summands = []
    for gt in GT:
        print(gt)
        ice_model = Ice(gt)
        count = ice_model.fill_ice(gt, "alt")
        terms, monomial = to_latex(count)
        print(monomial)
        summands.append(monomial)
    print('\n')
    print('+ '.join(summands))

