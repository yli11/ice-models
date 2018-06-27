#! /usr/bin/env python3
import argparse
import sys

class Ice:
    """ An ice object is associated with a list of vertices, can be accessed by their indices
        Args:
            GT: a list of lists
            vertices: a list of Vertex objects

    """
    def __init__(self, GT):
        self.nrows = len(GT)
        self.ncols = GT[0][0]+1
        self.vertices = []
        for i in range(1, self.nrows+1):
            row = []
            for j in range(self.ncols):
                v = Vertex(i, self.ncols-1-j)
                row.append(v)
            self.vertices.append(row)

    def get_vertex(self, i, j):
        """ get the vertex indexed by (i, j) """
        if 1 <= i <= self.nrows and 0 <= j < self.ncols:
            v = self.vertices[i-1][-1-j]
            assert(v.x==i and v.y==j)
            return v
        else:
            return None



    def fill_ice(self, GT, ice_type="square"):
        """ Start filling the ice model from the top-left corner.
            Print result if successful (not implemented yet), otherwise, display an error message
            Note: This process only change edges where no arrows have been placed (i.e. labeled by 0)
        """
        
        # create boundary conditions of square ice
        if ice_type == "square":
            for i in range(1, self.nrows+1):
                left_v = self.get_vertex(i, self.ncols-1)
                left_v.change_left(-1)
                right_v = self.get_vertex(i, 0)
                right_v.change_right(-1)
            for i in range(self.ncols):
                bottom_v = self.get_vertex(self.nrows, i)
                bottom_v.change_down(1)

        # create boundary conditions when row i and \bar i have alternating signs on the right end
        elif ice_type == "alt":
            for i in range(1, self.nrows+1):
                left_v = self.get_vertex(i, self.ncols-1)
                left_v.change_left(-1)
                right_v = self.get_vertex(i, 0)
                if i % 2 ==0:
                    right_v.change_right(1)
                else:
                    right_v.change_right(-1)
            for i in range(self.ncols):
                bottom_v = self.get_vertex(self.nrows, i)
                bottom_v.change_down(1)

        # start filling ice models based on the GT pattern
        try:
            for i in range(1, self.nrows+1):
                for j in range(self.ncols-1, -1, -1):
                    current_v = self.get_vertex(i, j)
                    if j in GT[i-1]:
                        current_v.change_up(1)
                    else:
                        current_v.change_up(-1)
        except:
            print("vertex "+str(i)+","+str(j)+" went wrong during initialization")
            return current_v

        # fill in the remaining arrows
        for i in range(1, self.nrows+1):
            for j in range(self.ncols-1, -1, -1):
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
                    print("Ugh... No legal ice model is found.")
                    print("Process failed at row " +str(current_v.x) + ", column " + str(current_v.y))
                    exit(-1)
        
        print("GT pattern has a valid ice model.")



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
            # if two arrows needs to be out and in, start from the one pointing out
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
    ice_model = Ice(GT)
    print("\nGT pattern received. Start filling ice model now. \n")
    return GT, ice_model



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Usage: python3 testIce.py <--alternating>. You will be prompted to enter the GT pattern.)')
    parser.add_argument('-a','--alternating', action='store_true',
                        help="whether we want the right most column to have alternating signs")
    args = parser.parse_args()
    GT, ice_model = parseGT()
    if args.alternating:
        ice_model.fill_ice(GT, "alt")
    else:
        ice_model.fill_ice(GT, "square")

