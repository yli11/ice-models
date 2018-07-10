from generateGT import *
from testIce import *
import sys
from sympy import *



def apply_weight(to_be_weighted, n):
    """ Plug in weights and check polynomial sum
    """
    Z = numbered_symbols('z')
    Z = [ next(Z) for i in range(2) ]
    t = symbols('t')
    summands = []
    try: 
        for monomial in to_be_weighted:
            prod = 1
            for var_term in monomial:

                # same for bar and no-bar rows
                if var_term[1] == 1 or var_term[0] in ["NW", "EW", "B"]:
                    continue
                elif var_term[0] == 'SW':
                    prod *= t

                elif var_term[1] % 2 == 0: #bar rows
                    if var_term[0] == 'NE' or var_term[0] == 'SE':
                        prod *= (1/Z[-(var_term[1]//2 - 1)])**var_term[2]
                    elif var_term[0] == 'NS':
                        x = (Z[-(var_term[1]//2 - 1)]*(t+1))**var_term[2]
                        prod *= ((1/Z[-(var_term[1]//2 - 1)])*(t+1))**var_term[2]
                    elif var_term[0] == "A":
                        prod *= Z[-(var_term[1]//2 - 1)]**2
                    else:
                        print("Something's wrong with the ice model...", var_term[0])
                        exit(-1)

                else: #non-bar rows
                    if var_term[0] == 'NE' or var_term[0] == 'SE':
                        prod *= Z[-(var_term[1]//2 - 1)]**var_term[2]
                    elif var_term[0] == 'NS':
                        prod *= (Z[-(var_term[1]//2 - 1)]*(t+1))**var_term[2]
            #print(expand(prod))
            summands.append(prod)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("The following term can't be evaulated:", end=' ')
        print(var_term)

    result = 0
    for t in summands:
        result += t
    return factor(expand(result))


def to_latex(count):
    """ Return a list of factors and the product of all terms as LaTex-format strings
        Directions of inward arrows: NE, SW, NW, SE, NS, EW
    """
    terms = []
    var_names = {(-1,-1,1,1):'NE', (1,1,-1,-1):'SW', (-1,1,1,-1):'NW', (1,-1,-1,1):'SE', (-1,1,-1,1):'NS', (1,-1,1,-1):'EW', (1,-1): "A", (-1,1): "B"}
    for i, row in enumerate(count):
        reduced = {x:y for x,y in row.items() if y!=0}
        for key, val in reduced.items():
            terms.append([var_names[key], i+1, val])
    latex = ''.join(term[0]+"_"+ str(term[1])+"^"+str(term[2])+' ' for term in terms)
    return terms, latex

if __name__ == "__main__":
    text = input("Please enter the top row of the GT pattern:")
    top_row = [int(x) for x in text.split()]
    GT = OrthogonalGTPatterns(top_row,False)
    summands = []
    to_be_weighted = []
    for gt in GT:
        print(gt)
        try:
            ice_model = Ice(gt)
            count = ice_model.fill_ice(gt, "alt")
            ice_model.visualize()
            terms, monomial = to_latex(count)
            #print(monomial)
            summands.append(monomial)
            to_be_weighted.append(terms)
        except :
            print("The following patterns does not have a corresponding ice model:")
            print(gt)
            pass
    print('# of patterns: ' +str(len(list(GT))))
    #print('+ '.join(summands))

    result = apply_weight(to_be_weighted, len(top_row) - 1)
    print(result)

