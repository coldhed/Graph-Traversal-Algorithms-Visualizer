from collections import deque
from util.Node import Node

# greedy first search using manhattan distance as a heuristic

class GFS:
    def __init__(self, start, target, grid):
        self.start = start # start is a tuple (x, y)
        self.target = target
        self.grid = grid # grid is an array where grid[y][x] tells you if it is a wall (true) or a tile (false)
        
        self.width = len(self.grid[0]) - 1
        self.height = len(self.grid) - 1

        self.current = Node(*self.start, []) # pass an empty path

        # seen[y][x] tells you if it has been seen before (true) or not (false)        
        self.seen = set()
        
        self.path = [] # keeps track of the path to the current node
        
        # append at the right and pop from the right
        self.s = deque([self.current])
        
    def getCurrent(self):
        return (self.current.x, self.current.y)
    
    def getNeighbors(self, x, y):
        neighbors = []
        
        # neighbors if they are in bound, and they have not been seen before, and they are not walls     
        if (x - 1 >= 0) and (x - 1, y) not in self.seen and self.grid[y][x-1] == False:
            neighbors.append((x-1, y))
            
        if (y - 1 >= 0) and (x, y - 1) not in self.seen and self.grid[y-1][x] == False:
            neighbors.append((x, y-1))
            
        if (y + 1 <= self.height) and (x, y + 1) not in self.seen and self.grid[y+1][x] == False:
            neighbors.append((x, y+1))
            
        if (x + 1 <= self.width) and (x  + 1, y) not in self.seen and self.grid[y][x+1] == False:
            neighbors.append((x+1, y))
        
            
        return neighbors
            
        
        
         
        
    def stepSearch(self):
        if self.s: # if its not empty
            self.current = self.s.pop()
            x = self.current.x
            y = self.current.y
            
            self.path = self.current.path
            
            
            # check if we reached target
            if (x, y) == self.target:
                return 1
            
            tmpPath = list(self.path)
            tmpPath.append((x, y))
            
            # order from worst to best (so that best is in the top of the stack)
            for neighbor in self.order(self.getNeighbors(x, y)):
                tmpX, tmpY = neighbor
                self.seen.add((tmpX, tmpY))
                
                n = Node(tmpX, tmpY, tmpPath)
                self.s.append(n)
                
            return 0
            
        else:
            return -1
        
    def order(self, nodes):
        # base case
        if len(nodes) <= 1: return nodes
        
        nDistance = {} # dict of nums to distances
        
        for node in nodes:
            nDistance[node] = self.manhattanDistance(node)
    
        # return a list of nDistance keys sorted by the values in descending order
        return list(sorted(nDistance, key=nDistance.get, reverse=True))
            

    def manhattanDistance(self, node):
        # returns the manhattan distance of a node to the target
        # if node -> (w1, h1)
        # and target -> (w2, h2)
        
        # manhattan distance is = |w2-w1|+|h2-h1|
        w1, h1 = node
        w2, h2 = self.target
        
        return abs(w2 - w1) + abs(h2 - h1)
