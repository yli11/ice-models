from generateGT import *
from testIce import *
import sys
from sympy import *



def apply_weight(to_be_weighted, n):
    """ Plug in weights and check polynomial sum
    """
    Z = numbered_symbols('z')
    Z = [ next(Z) for i in range(n) ]
    t = symbols('t')
    summands = []
    try: 
        for monomial in to_be_weighted:
            prod = 1
            for var_term in monomial:
                # extract row index and exponents, note: i starts from 0
                i = int((var_term[1]+0.5)//2) - 1
                exp = var_term[2]

                # same for bar and no-bar rows
                if var_term[1] == 1 or var_term[0] in ["NW", "EW"]:
                    continue
                elif var_term[1] == 1 and var_term[0] == 'NE':
                    prod *= 0

                elif var_term[1] % 2 == 0: #bar rows
                    if var_term[0] == 'SE':
                        prod *= (t*Z[i])**exp
                    elif var_term[0] == 'NE':
                        prod *= (Z[i])**exp
                    elif var_term[0] == 'NS':
                        prod *= (Z[i]*(t+1))**exp
                    elif var_term[0] == 'SW':
                        prod *= 1

                    elif var_term[0] == "A": # U-turn vertices are associated with bar rows
                        prod *= (1/Z[i])*(1+t*Z[i])/(1+t*Z[i]**2)
                    elif var_term[0] == 'B':
                        prod *= t*Z[i]*(1+t*Z[i])/(1+t*Z[i]**2)
                    else:
                        print("Something's wrong with the ice model...", var_term[0])
                        exit(-1)

                else: #non-bar rows
                    if var_term[0] == 'SE':
                        prod *= Z[i]**(-exp)
                    elif var_term[0] == 'NE':
                        prod *= Z[i]**(-exp)
                    elif var_term[0] == 'NS':
                        prod *= (Z[i]**(-1)*(t+1))**exp
                    elif var_term[0] == 'SW':
                        prod *= t**exp

            #print(expand(prod))
            summands.append(prod)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("The following term can't be evaulated:", end=' ')
        print(var_term)

    result = 0
    for t in summands:
        result += t
    return expand(result)

def apply_weight_indexed(to_be_weighted, n):
    """ Plug in weights and check polynomial sum
    """
    Z = numbered_symbols('z')
    T = numbered_symbols('t')
    Z = [ next(Z) for i in range(n) ]
    T = [ next(T) for i in range(n) ]
    summands = []
    try: 
        for monomial in to_be_weighted:
            #print(monomial)
            prod = 1
            for var_term in monomial:
                i = int((var_term[1]+0.5)//2)
                exp = var_term[2]

                # same for bar and no-bar rows
                if var_term[1] == 1 or var_term[0] in ["NW", "EW", "B"]:
                    continue

                elif var_term[1] % 2 == 0: #bar rows
                    if var_term[0] == 'SE':
                        prod *= (1/Z[i])**exp
                    elif var_term[0] == 'NE':
                        prod *= (1/Z[i])**exp
                    elif var_term[0] == 'NS':
                        prod *= ((1/Z[i])*(T[i]+1))**exp
                    elif var_term[0] == 'SW':
                        prod*= T[i]**exp

                    elif var_term[0] == "A":
                        prod *= Z[i]**2
                    else:
                        print("Something's wrong with the ice model...", var_term[0])
                        exit(-1)

                else: #non-bar rows
                    if var_term[0] == 'SE':
                        prod *= Z[i]**(-exp)
                    elif var_term[0] == 'NE':
                        prod *= Z[i]**(-exp)
                    elif var_term[0] == 'NS':
                        prod *= (Z[i]*(T[i]+1))**exp
                    elif var_term[0] == 'SW':
                        prod *= T[i]**exp
                    else:
                        print("Something's wrong with the ice model...", var_term[0])
                        exit(-1)
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

def apply_weight_kt(to_be_weighted, n):
    """ Plug in weights and check polynomial sum
    """
    Z = numbered_symbols('z')
    Z = [ next(Z) for i in range(n) ]
    t = symbols('t')
    a, b, c = symbols('a:c')
    summands = []
    try: 
        for monomial in to_be_weighted:
            prod = 1
            for var_term in monomial:
                # extract row index and exponents, note: Z[i] gives z_i
                i = var_term[1]//3 - n
                exp = var_term[2]

                #Do we care about ties
                bents = {"A":Z[i]**2, "B":1, "C":0}
                if var_term[0] in bents:
                    prod *= bents[var_term[0]]


                # same for bar and no-bar rows
                elif var_term[1]%3 == 0 or var_term[0] in ["NW", "EW"]:
                    continue

                    """ YBE
                    Even: SW + SW*NE = NS
                    Odd: SE + SW*NE = NS
                    """   
                elif var_term[1] % 3 == 2: #bar rows (even)
                    if var_term[0] == 'SE':
                        prod *= (Z[i]*t)**exp
                    elif var_term[0] == 'NE':
                        prod *= (Z[i])**exp
                    elif var_term[0] == 'NS':
                        prod *= (Z[i]*(t+1))**exp
                    elif var_term[0] == 'SW':
                        prod *= 1

                else: #double-bar rows (odd)
                    if var_term[0] == 'SE':
                        prod *= Z[i]**(-exp)
                    elif var_term[0] == 'NE':
                        prod *= Z[i]**(-exp)
                    elif var_term[0] == 'NS':
                        prod *= (Z[i]**(-1)*(t+1))**exp
                    elif var_term[0] == 'SW':
                        prod *= t**exp

            #print(expand(prod))
            summands.append(prod)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("The following term can't be evaulated:", end=' ')
        print(var_term)

    result = 0
    for t in summands:
        result += t
    return expand(result)


def to_latex(count):
    """ Return a list of factors and the product of all terms as LaTex-format strings
        Directions of inward arrows: NE, SW, NW, SE, NS, EW
        Returns:
            terms (list): e.g.['SW', 1, 1]
            latex(string)
    """
    terms = []
    var_names = {(-1,-1,1,1):'NE', (1,1,-1,-1):'SW', (-1,1,1,-1):'NW', (1,-1,-1,1):'SE', (-1,1,-1,1):'NS', (1,-1,1,-1):'EW', (1,-1): "A", (-1,1): "B", (1,1):"C", (1,-1,'t'):"U", (-1,1,'t'):"D", (1,1,'t'):"O"}
    for i, row in enumerate(count):
        reduced = {x:y for x,y in row.items() if y!=0}
        for key, val in reduced.items():
            terms.append([var_names[key], i+1, val])
    latex = ''.join(term[0]+"_"+ str(term[1])+"^"+str(term[2])+' ' for term in terms)
    return terms, latex

def irr_terms(monomials):
    """ 
    Params:
        monomials (list): each entry is var_term (list)
    Returns:
        a list of directions that do not appear in the corresponding ice states
    """
    all_types = ['NE', 'SW', 'NW','SE','NS','EW']
    reduced = [monomial for monomial in monomials if "C" not in [var_term[0] for var_term in monomial]]
    vertex_types_e = [var_term[0] for monomial in monomials for var_term in monomial if var_term[1]%3==0]
    vertex_types_o = [var_term[0] for monomial in monomials for var_term in monomial if var_term[1]%3==1]
    return [[vertex_type for vertex_type in all_types if vertex_type not in vertex_types_o],\
            [vertex_type for vertex_type in all_types if vertex_type not in vertex_types_e]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Usage: python3 main.py <pattern> <-i> <-f>')
    parser.add_argument('-i','--index', action='store_true',
                        help="Replace uniform t with t_i's based on the row index of the vertex.")
    parser.add_argument('-f','--factor', action='store_true',
                        help="Return factored result.")
    parser.add_argument('--KT', action='store_true',
                        help="Calculate partition function for KT ice instead.")
    parser.add_argument('input', nargs='+', type=int, help='Top row of the GT pattern.')
    args = parser.parse_args()

    #text = input("Please enter the top row of the GT pattern:")
    top_row = args.input #[int(x) for x in text.split()]
    #top_row = [int(x) for x in text.split()]
    if args.KT:
        GT = OrthogonalGTPatterns(top_row, True, 1)
    else:
        GT = OrthogonalGTPatterns(top_row, True, 0)
    summands = []
    to_be_weighted = []
    for gt in GT:
        #print(gt)
        if args.KT:
            ice_model = Ice(gt, "KT")
        else:
            ice_model = Ice(gt, "alt")
        count = ice_model.fill_ice(gt)
        #ice_model.visualize()
        terms, monomial = to_latex(count)
        #print(monomial, '\n')
        summands.append(monomial)
        to_be_weighted.append(terms)

    print('# of patterns: ' + str(len(list(GT))))
    #print('+ '.join(summands))
    if args.index:
        result = apply_weight_indexed(to_be_weighted, len(top_row) - 1)
    if args.KT:
        result = apply_weight_kt(to_be_weighted, len(top_row))
        irrelevance = irr_terms(to_be_weighted)
        print("\nNot in odd rows:", irrelevance[0])
        print("Not in even rows:", irrelevance[1], '\n')
    else:
        result = apply_weight(to_be_weighted, len(top_row) - 1)
    if args.factor:
        print(factor(result))
    else:
        print(result)

