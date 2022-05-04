from enum import IntEnum

# You can get the enumeration based on integer value, or make comparison
# ex: d = Direction(1), then d would be Direction.NORTH
# ex: print(Direction.SOUTH == 1) should return False
class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST  = 3
    EAST  = 4

# Construct class Node and its member functions
# You may add more member functions to meet your needs
class Node:
    def __init__(self, row):
        self.index = int(row[0])
        self.neighbors = []
        self.neighborsD = []
        for i in range(1, 5):
            if row[i] > 0:
                self.neighbors.append(int(row[i]))
            else:
                self.neighbors.append(-1)
        for i in range(5, 9):
            if row[i] > 0:
                self.neighborsD.append(int(row[i]))
            else:
                self.neighborsD.append(-1)
        # store successor as (Node, direction to node, distance)
        self.Successors = [-1]
        self.distance = 0
        self.terminal = self.isTerminal()

    def getIndex(self):
        return self.index

    def getSuccessors(self):
        return self.Successors

    def setSuccessor(self, successor, direction, length=1):
        self.Successors.append((successor, Direction(direction), int(length)))
        print("For Node {}, a successor {} is set.".format(self.index, self.Successors[-1]))
        return


    def getDirection(self, nd):
        # TODO : if nd is adjacent to the present node, return the direction of nd from the present node
		# For example, if the direction of nd from the present node is EAST, then return Direction.EAST = 4
		# However, if nd is not adjacent to the present node, print error message and return 0 
        return

    def isSuccessor(self, nd):
        for succ in self.Successors:
            if succ[0] == nd: 
                return True
        return False
    
    def isTerminal(self):
        b = 0
        for adj in self.neighbors:
            if adj == -1:
                b = b + 1
        if b == 3:
            return True
        else:
            return False

    def print(self):
        print(self.index, self.neighbors, self.neighborsD, self.Successors)

