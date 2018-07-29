#! /usr/bin/env python3
import argparse
import sys

class Ice:
    """ An ice object is associated with a list of vertices, can be accessed by their indices
        Args:
            GT: a list of lists
            vertices: a list of Vertex objects
            ice_type (string): options include {"square", "alt", "KT"}
    """

    def __init__(self, GT, ice_type="alt"):
        self.nrows = len(GT)
        self.ncols = GT[0][0]
        self.vertices = []
        self.ice_type = ice_type
        for i in range(0, self.nrows):
            row = [Vertex(i+1, self.ncols-j) for j in range(0, self.ncols)]
            self.vertices.append(row)

    def get_vertex(self, i, j):
        """ get the vertex indexed by (i, j) """
        if 0 <= i <= self.nrows and 1 <= j <= self.ncols:
            v = self.vertices[i-1][-j]
            assert(v.x==i and v.y==j)
            return v
        else:
            return None



    def fill_ice(self, GT):
        """ Start filling the ice model from the top-left corner.
            If ice modeled is succesfully filled out, print result and tally ice states;
            display an error message otherwise.
            Note: This process only changes edges where no arrows have been placed (i.e. labeled by 0)
        """
        
        # create boundary conditions of square ice
        # defunct now since columns start with 1
        # can be changed similarly as the alternating case
        if self.ice_type == "square":
            if 0 in [elt for row in GT for elt in row]:
                print("Current model doesn't have column 0. Please add 1 to all entries for square ice.\n")
                exit(0)
            for i in range(1, self.nrows+1):
                left_v = self.get_vertex(i, self.ncols)
                left_v.change_left(-1)
                right_v = self.get_vertex(i, 1)
                right_v.change_right(-1)
            for i in range(1, self.ncols+1):
                bottom_v = self.get_vertex(self.nrows, i)
                bottom_v.change_down(1)

        # create boundary conditions when row i and \bar i have alternating signs on the right end
        elif self.ice_type == "alt" or self.ice_type == "KT":
            for i in range(1, self.nrows+1):
                left_v = self.get_vertex(i, self.ncols)
                left_v.change_left(-1)
            # not initiating right most column, since it's uniquely determined by the # of row entries
            for i in range(1, self.ncols+1):
                bottom_v = self.get_vertex(self.nrows, i)
                bottom_v.change_down(1)

        # start filling ice models based on the GT pattern
        try:
            for i in range(1, self.nrows+1):
                for j in range(self.ncols, 0, -1):
                    current_v = self.get_vertex(i, j)
                    if j in GT[i-1]:
                        current_v.change_up(1)
                    else:
                        current_v.change_up(-1)
        except:
            raise ValueError("vertex "+str(i)+","+str(j)+" went wrong during initialization")
            return current_v

        # fill in the remaining arrows
        for i in range(1, self.nrows+1):
            for j in range(self.ncols, 0, -1):
                # first, load the adjacent arrows from initialization (all upward arrows should already be filled at this point, arrows right of the current vertex should be empty except for the right boundary)
                current_v = self.get_vertex(i, j)
                if self.get_vertex(i+1, j):
                    down = self.get_vertex(i+1, j).up
                    current_v.change_down(-down)
                if self.get_vertex(i, j+1):
                    left = self.get_vertex(i, j+1).right
                    current_v.change_left(-left)
                changed = current_v.fill_all()
                if not changed:
                    #print("Ugh... No legal ice model is found.")
                    self.visualize()
                    raise ValueError("Process failed at row " +str(current_v.x) + ", column " + str(current_v.y))
        
        #print("GT pattern has a valid ice model.\n")
        count = self.tally()
        return count


    def visualize(self):
        up_arrows = {1:'\u2191', -1:'\u2193', 0:'\u2753'}
        left_arrows = {1:'\u2190', -1: '\u2192', 0:'\u2753'}
        right_arrows = {1:'\u2192', -1:'\u2190', 0:'\u2753'}
        down_arrows = {1:'\u2193', -1:'\u2191', 0:'\u2753'}
        for row in self.vertices:
            print(''.join(["   " + up_arrows[v.up]+ "  " for v in row]))
            for v in row:
                print(left_arrows[v.left]+"("+str(v.x)+","+str(v.y)+")",end='')
                if v.y == 1:
                    if self.ice_type == "KT" and v.x % 3 == 0:
                        print()
                    else:
                        print(right_arrows[v.right])
            if row[0].x == self.nrows:
                print(''.join(["   " + down_arrows[v.down]+ "  " for v in row]+["\n"]))


    def tally(self):
        # directions of inward arrows: NE, SW, NW, SE, NS, EW
        # represented as a tuple in clockwise order (NESW)
        count = []
        for row in self.vertices:
            count_row = {(-1,-1,1,1):0, (1,1,-1,-1):0, (-1,1,1,-1):0, (1,-1,-1,1):0, (-1,1,-1,1):0, (1,-1,1,-1):0, (1,-1): 0, (-1,1): 0, (1,1):0,(1,1,'t'):0,(1,-1,'t'):0,(-1,1,'t'):0}
            for v in row:
                count_row[(v.up, v.right, v.down, v.left)] += 1
                # counting U-turn vertices
                if self.ice_type == 'alt':
                    if v.x % 2 == 0 and v.y == 1:
                        right_arr_1 = v.right
                        right_arr_2 = self.get_vertex(v.x+1, 1).right
                        count_row[(right_arr_1, right_arr_2)] += 1
                # count ties for KT ice
                elif self.ice_type == "KT":
                    if v.x % 3 == 1 and v.y == 1:
                        right_arr_1 = v.right
                        right_arr_2 = self.get_vertex(v.x+1, 1).right
                        count_row[(right_arr_1, right_arr_2)] += 1
                    if v.x % 3 == 0 and v.y == 1:
                        count_row[(v.up, v.down,'t')] += 1
            count.append(count_row)
        return count


class Vertex:
    """A vertex has four arrows
       Args:
            x, y: coordinates of the vertex
            up, down, left, right: -1 means "arrow pointing in", 1 means "out"
            
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

    def change_left(self, val):
        if self.left == 0:
            self.left = val

    def change_right(self, val):
        if self.right == 0:
            self.right = val

    def change_up(self, val):
        if self.up == 0:
            self.up = val

    def change_down(self, val):
        if self.down == 0:
            self.down = val

    def fill_all(self):
        vals = [self.up, self.down, self.left, self.right]
        diff = - sum(vals)
        zeros = [i for i, x in enumerate(vals) if x == 0]
        if len(zeros) != abs(diff) and not (diff==0 and len(zeros)%2==0):
            return False
        else:
            directions = {0: Vertex.change_up, 1: Vertex.change_down, 2: Vertex.change_left, 3: Vertex.change_right}
            # fill in the arrows in the order up-down-left-right
            # if two arrows need to be out and in, respectively, start from the one pointing out
            for k in zeros:
                f = directions[k]
                if diff > 0:
                    f(self, 1)
                    diff -= 1
                else:
                    f(self, -1)
                    diff += 1

            assert(diff==0)
            return True


def parseGT():
    GT = []
    text = input("Please enter the first line of your GT pattern, separated by whitespaces:")
    while text != "":
        GT.append([int(x) for x in text.split()])
        text = input("Please enter the next line of of the GT pattern:")
    print("\nGT pattern received. Start filling ice model now. \n")
    return GT



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Usage: python3 testIce.py <--alternating>. You will be prompted to enter the GT pattern.)')
    parser.add_argument('-a','--alternating', action='store_true',
                        help="whether we want the right most column to have alternating signs")
    args = parser.parse_args()
    GT = parseGT()
    if args.alternating:
        ice_model = Ice(GT, "alt")
        count = ice_model.fill_ice(GT)
        ice_model.visualize()
    else:
        ice_model = Ice(GT, "square")
        count = ice_model.fill_ice(GT)
        ice_model.visualize()

    for row, row_count in enumerate(count):
        print("Row " + str(row+1) + ": ", end='') 
        print("NE = " + str(row_count[(-1,-1,1,1)]), end='; ')
        print("SW = " + str(row_count[(1,1,-1,-1)]), end='; ')
        print("NW = " + str(row_count[(-1,1,1,-1)]), end='; ')
        print("SE = " + str(row_count[(1,-1,-1,1)]), end='; ')
        print("NS = " + str(row_count[(-1,1,-1,1)]), end='; ')
        print("EW = " + str(row_count[(1,-1,1,-1)]), end='; ')
        print("A = " + str(row_count[(1,-1)]), end='; ')
        print("B = " + str(row_count[(-1,1)]))

    print('\n')

