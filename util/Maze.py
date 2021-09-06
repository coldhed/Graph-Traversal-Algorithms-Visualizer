# following algorithm described by the answer: 
# https://stackoverflow.com/questions/22305644/how-to-generate-a-maze-with-more-than-one-successful-path

# steps:
#     1. Create a grid where odd rows and columns are walls
#     2. Create two sets: origin, target, undiscovered
#      - the sets store cells in a (w, h) tuple
#     3. At random, remove a wall that reveals a cell from undiscovered and adds it to either origin or target set
#      - the wall has to be even in one h or w coordinate -> (odd, odd) will never be removed for it to look more "mazey"
#     4. When there are no cells from undiscovered, remove x walls that connect origin to target
#      - x is the number of solutions that there'll be

import random

class Maze():
    def __init__(self, width, height, origin, target):
        self.width = width
        self.height = height
        
        
        self.origin = set([origin])
        self.target = set([target])
        
        self.undiscovered = set()
        self.walls = set()
        
        # populate the undiscovered set with all empty cells that are not the origin or the target
        for w in range(0, self.width, 2):
            for h in range(0, self.height, 2):
                if (w, h) != origin and (w, h) != target:
                    self.undiscovered.add((w,h))
                
        # populate walls set with walls
            # columns
        for w in range(1, self.width, 2):
            for h in range(0, self.height):
                self.walls.add((w,h))
            # rows
        for h in range(1, self.height, 2):
            for w in range(0, self.width):
                self.walls.add((w,h))

        # used to determine were we can break through    
        #   - frontier is a list of walls we can potentially break    
        self.originFrontier = set(self.getFrontier(origin))
        self.targetFrontier = set(self.getFrontier(target))
        
        
        # if the origin or the target are in a spot where a wall goes -> remove the wall and update sets
        self.checkNodesInWall(origin, target)
        
    #       M A I N   A L G O R I T H M   F U N C T I O N
    def createMaze(self, n_of_solutions):
        # step 3
        self.removeWalls()
        
        # step 4
        self.addSolutions(n_of_solutions)

        # optional step -> when the last column / row is a wall the algorithm doesnt remove it so it ends up looking odd
        self.fixOddWalls()
        
        return self.setsToGrid()
                
    def checkNodesInWall(self, origin, target):
        w, h = origin
        if not (w % 2 == 0 and h % 2 == 0):
            self.walls.remove(origin)
            
            if w % 2 == 0 or h % 2 == 0: # in a removeable wall
                if (w+1, h) in self.undiscovered:
                    self.undiscovered.remove((w+1, h))
                    self.origin.add((w+1, h))
                    self.originFrontier.update(self.getFrontier((w+1, h)))
                if (w-1, h) in self.undiscovered:
                    self.undiscovered.remove((w-1, h))
                    self.origin.add((w-1, h))
                    self.originFrontier.update(self.getFrontier((w-1, h)))
                if (w, h+1) in self.undiscovered:
                    self.undiscovered.remove((w, h+1))
                    self.origin.add((w, h+1))
                    self.originFrontier.update(self.getFrontier((w, h+1)))
                if (w, h-1) in self.undiscovered:
                    self.undiscovered.remove((w, h-1))
                    self.origin.add((w, h-1))
                    self.originFrontier.update(self.getFrontier((w, h-1)))
                
                # otherwise origin is in a non removable wall but we remove it and the frontier is already correct
                
        w, h = target
        if not (w % 2 == 0 and h % 2 == 0):
            self.walls.remove(target)
            
            if w % 2 == 0 or h % 2 == 0: # in a removeable wall
                if (w+1, h) in self.undiscovered:
                    self.undiscovered.remove((w+1, h))
                    self.target.add((w+1, h))
                    self.targetFrontier.update(self.getFrontier((w+1, h)))
                if (w-1, h) in self.undiscovered:
                    self.undiscovered.remove((w-1, h))
                    self.target.add((w-1, h))
                    self.targetFrontier.update(self.getFrontier((w-1, h)))
                if (w, h+1) in self.undiscovered:
                    self.undiscovered.remove((w, h+1))
                    self.target.add((w, h+1))
                    self.targetFrontier.update(self.getFrontier((w, h+1)))
                if (w, h-1) in self.undiscovered:
                    self.undiscovered.remove((w, h-1))
                    self.target.add((w, h-1))
                    self.targetFrontier.update(self.getFrontier((w, h-1)))
                
                # otherwise target is in a non removable wall but we remove it and the frontier is already correct
                
        
    
    
    
    def removeWalls(self):
        while (self.undiscovered): # loop until all cells are either in origin or target
                     
            if self.originFrontier:
                wall = random.choice(list(self.originFrontier))
                
                newTiles = self.tileIfRemoveWall(wall)

                if newTiles:
                    self.walls.remove(wall)

                    for newTile in newTiles:
                        # add new discoverd tile to origin and delete it from discovered
                        self.undiscovered.remove(newTile)
                        self.origin.add(newTile)
                        
                        # add new discovered frontiers to originFrontier
                        self.originFrontier.update(self.getFrontier(newTile))
                
                else: 
                    # that wall didnt discover a newTile
                    self.originFrontier.remove(wall)
                
            if self.targetFrontier:
                wall = random.choice(list(self.targetFrontier))
                
                newTiles = self.tileIfRemoveWall(wall)

                if newTiles:
                    self.walls.remove(wall)

                    for newTile in newTiles:
                        # add new discoverd tile to target and delete it from discovered
                        self.undiscovered.remove(newTile)
                        self.target.add(newTile)
                        
                        # add new discovered frontiers to targetFrontier
                        self.targetFrontier.update(self.getFrontier(newTile))
                
                else: 
                    # that wall didnt discover a newTile
                    self.targetFrontier.remove(wall)
                

    def addSolutions(self, n_of_solutions):
        while(n_of_solutions > 0):            
            wall = random.choice(list(self.walls))
            
            if self.connectsFrontiers(wall):
                self.walls.remove(wall)
                n_of_solutions -= 1
    
    def connectsFrontiers(self, wall):
        # returns true if removing that wall connects the origin and target
        w, h = wall
        
        # try horizontally
        tile1 = (w - 1, h)
        tile2 = (w + 1, h)
        
        
        if (tile1 in self.origin and tile2 in self.target) or (tile1 in self.target and tile2 in self.origin):
            return True
        
        # try vertically
        tile1 = (w, h - 1)
        tile2 = (w, h + 1)
        
        if (tile1 in self.origin and tile2 in self.target) or (tile1 in self.target and tile2 in self.origin):
            return True
        
        return False
    
    def setsToGrid(self):
        # returns a 2d set where False is a tile and True is a wall
        grid = []
        for h in range(self.height):
            row = []
            for w in range(self.width):
                if (w, h) in self.walls:
                    row.append(True)
                else: 
                    row.append(False)
            
            grid.append(row)
        
        return grid

    def getFrontier(self, tile):
        # given a tile, return a list of all walls neigboring that tile
        frontier = [] # list is used so that it can be unpacked with the *frontier operator
        w, h = tile
        
        
        if (w+1, h) in self.walls and self.canRemove((w+1, h)): frontier.append((w+1,h))
        if (w-1, h) in self.walls and self.canRemove((w-1, h)): frontier.append((w-1, h))
        if (w, h+1) in self.walls and self.canRemove((w, h+1)): frontier.append((w, h+1))
        if (w, h-1) in self.walls and self.canRemove((w, h-1)): frontier.append((w, h-1))
        
        return frontier
    
    def canRemove(self, tile):
        # returns true if wall is not odd_w, odd_h
        
        w, h = tile
        
        if (w % 2) != 0 and (h % 2) != 0:
            return False
        else:
            return True

        
    
    def tileIfRemoveWall(self, wall):
        # return undiscoverd if removing the wall discovers a undiscovered tile
        w, h = wall
        
        walls = list()
        
        if (w+1, h) in self.undiscovered: walls.append((w+1, h))
        if (w-1, h) in self.undiscovered: walls.append((w-1, h))
        if (w, h+1) in self.undiscovered: walls.append((w, h+1))
        if (w, h-1) in self.undiscovered: walls.append((w, h-1))
        
        return walls

    def fixOddWalls(self):
        # you could do it at random but this technique is more efficient and it looks good
        
        if (self.width - 1) % 2 != 0:
            for w in range(0, self.width, 4):
                if (w, self.height-1) in self.walls:
                    self.walls.remove((w, self.height-1))
                
        if (self.height - 1) % 2 != 0:
            for h in range(0, self.height, 4):
                if (self.width-1, h) in self.walls:
                    self.walls.remove((self.width-1, h))