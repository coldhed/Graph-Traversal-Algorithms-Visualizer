from util.Tile import Tile
from util.Button import Button
from util.Maze import Maze

from algorithms.BFS import BFS
from algorithms.DFS import DFS
from algorithms.GFS import GFS
from algorithms.AStar import AStar

from math import floor
import pygame

class Grid:
    def __init__(self, width, height, tile_w, colorPalette, 
                 line_w = 1, menuOffset = 0, txtSize = 42, nSolutions = 4, fpsFast = 45, fpsSlow = 10):
        self.WIDTH = width
        self.HEIGHT = height
        self.colorPalette = colorPalette
        self.Y_OFFSET = menuOffset
        self.LINE_W = line_w
        
        self.nSolutions = nSolutions
        self.fpsFast = fpsFast
        self.fpsSlow = fpsSlow

        self.TILE_W = tile_w # should be divisible by width and height so it all works out
        self.RECT_OFF = floor(self.LINE_W / 2) # offset due to the line's width
        
        # array of tiles
        self.tiles = []
        for h in range(0, self.HEIGHT, self.TILE_W):
            row = []
            for w in range(0, self.WIDTH, self.TILE_W):
                # menu offset is included in the height
                row.append(Tile(w, h + self.Y_OFFSET, self.TILE_W, self.RECT_OFF))
            self.tiles.append(row)
                
        # array of buttons
        pygame.font.init()
        bigFont = pygame.font.SysFont('Calibri', txtSize)
        
        self.algButtons = [
            Button(110, 50, "Depth FS", bigFont, self.colorPalette),
            Button(315, 50, "Breadth FS", bigFont, self.colorPalette),
            Button(530, 50, "Greedy FS", bigFont, self.colorPalette),
            Button(740, 50, "A-Star", bigFont, self.colorPalette)
        ]
        
        smallFont = pygame.font.SysFont('Calibri', floor(txtSize / 2))
        
        self.otherButtons = {
            "Maze" : Button(110, 150, "Generate Maze", smallFont, self.colorPalette),
            "Clear" : Button(280, 150, "Clear", smallFont, self.colorPalette),
            "Slow"  : Button(725, 150, "Slow", smallFont, self.colorPalette),
            "Fast" : Button(800, 150, "Fast", smallFont, self.colorPalette)
        }
        
        self.otherButtons["Slow"].highlightTrue()
        self.FPS = self.fpsSlow
        
        
        
        # origin and target tile -> for dragging them
        self.originTile = self.tiles[0][0]
        self.originTile.updateState("origin")
        
        self.targetTile = self.tiles[-1][-1]
        self.targetTile.updateState("target")
        
        # maze generator
        self.mazeGen = None
        
        # for mouse dragging
        self.leftBeingClicked = False
        self.rightBeingClicked = False
        self.originDragged = False
        self.targetDragged = False
        
        # algorithm selected stores the selected button representing the choice of algorithm
        self.algorithmSelected = None
        self.updateAlgorithm(self.algButtons[0])
        
        # algorithm is the algorithm object in itself
        self.algorithm = None
        
        
        self.solved = False
        
    def draw(self, screen):
        self.drawGrid(screen)
        self.drawTiles(screen)
        self.drawButtons(screen)
        
    def update(self, state):
        # DRAW STATE
        if state == "draw":
            (x, y) = pygame.mouse.get_pos()
            (xGrid, yGrid) = self.pixelsToGrid(x, y)
            
            if y > self.Y_OFFSET:
                clickedTile = self.tiles[yGrid][xGrid]
                
                if self.leftBeingClicked and clickedTile != self.originTile and clickedTile != self.targetTile:
                    clickedTile.updateState("wall")
                    
                elif self.rightBeingClicked and clickedTile != self.originTile and clickedTile != self.targetTile:
                    clickedTile.updateState("tile")
                    
                elif self.originDragged and clickedTile != self.targetTile: 
                    self.originTile.updateState("tile")
                    self.originTile = clickedTile
                    self.originTile.updateState("origin")
                    
                elif self.targetDragged and clickedTile != self.originTile:
                    self.targetTile.updateState("tile")
                    self.targetTile = clickedTile
                    self.targetTile.updateState("target")
        
        # SOLVE STATE
        elif state == "solve":
            if self.algorithm.stepSearch() == 1:
                self.solved = True
            
            self.updateTilesState(self.algorithm.seen, "seen")
            self.updateTilesState(self.algorithm.path, "path")
            self.updateTilesState([self.algorithm.getCurrent()], "current")
    
    
    
    def drawGrid(self, screen): 
        # + 1 so that the last lines are included
        for w in range(0, self.WIDTH + 1, self.TILE_W):
            pygame.draw.line(screen, self.colorPalette["DARKBLUE"], (w, self.Y_OFFSET), (w, self.HEIGHT + self.Y_OFFSET), self.LINE_W)
        
        for h in range(self.Y_OFFSET, self.HEIGHT + self.Y_OFFSET + 1, self.TILE_W):
            pygame.draw.line(screen, self.colorPalette["DARKBLUE"], (0, h), (self.WIDTH, h), self.LINE_W)
    
    def drawTiles(self, screen):
        for row in self.tiles:
            for tile in row:
                state = tile.getState()
                
                color = self.colorPalette["GRAY"] # default is gray
                
                # with python 3.10 a switch case statement would work 
                if state == "wall":
                    color = self.colorPalette["DARKBLUE"]
                
                elif state == "seen":
                    color = self.colorPalette["BLUE"]

                elif state == "path":
                    color = self.colorPalette["MINT"]
                
                elif state == "current":
                    color = self.colorPalette["ORANGE"]
                    
                elif state == "origin":
                        color = self.colorPalette["GREEN"]
                
                elif state == "target":
                    color = self.colorPalette["RED"]
                
                pygame.draw.rect(screen, color, tile.getRect())
                
    def drawButtons(self, screen):
        for button in self.algButtons:
            button.draw(screen)
            
        for key in self.otherButtons:
            self.otherButtons[key].draw(screen)
    
    def clickDown(self, x, y, left, state): # update tiles according to a click down and and x,y coord of the mouse
        # left argument is true if it was a left click, false if it was a right click
        if (y < self.Y_OFFSET):
            self.menuClick(x, y, state)
                    
        elif state == "draw":
            if self.originTile.wasItClicked(x, y):
                self.originDragged = True
                
            elif self.targetTile.wasItClicked(x, y):
                self.targetDragged = True
                
            elif left:
                self.leftBeingClicked = True
                
            else:
                self.rightBeingClicked = True
    
    def menuClick(self, x, y, state):
        if state == "draw":
            for button in self.algButtons:
                if button.clicked(x, y):
                    self.updateAlgorithm(button)
                    return
        
        if state == "draw":
            if self.otherButtons["Maze"].clicked(x, y): # generate a maze
                self.mazeGen = Maze(
                    len(self.tiles[0]), 
                    len(self.tiles), 
                    self.pixelsToGrid(*self.originTile.getPosition()), 
                    self.pixelsToGrid(*self.targetTile.getPosition())
                )
                
                newMap = self.mazeGen.createMaze(self.nSolutions)
                self.changeToNewMap(newMap)
            
            elif self.otherButtons["Clear"].clicked(x, y):
                self.changeToNewMap() # leave empty to clear it
        
        if self.otherButtons["Slow"].clicked(x, y):
            self.FPS = self.fpsSlow
            self.otherButtons["Slow"].highlightTrue()
            self.otherButtons["Fast"].highlightFalse()
            
        elif self.otherButtons["Fast"].clicked(x, y):
            self.FPS = self.fpsFast
            self.otherButtons["Fast"].highlightTrue()
            self.otherButtons["Slow"].highlightFalse()
            
    
    def changeToNewMap(self, newMap = None):
        if newMap == None:
            for h in range(len(self.tiles)):
                for w in range(len(self.tiles[0])):
                    if self.tiles[h][w] != self.originTile and self.tiles[h][w] != self.targetTile:
                        self.tiles[h][w].updateState("tile")
        else: 
            for h in range(len(newMap)):
                for w in range(len(newMap[h])):
                    if self.tiles[h][w] != self.originTile and self.tiles[h][w] != self.targetTile:
                        if newMap[h][w]:
                            self.tiles[h][w].updateState("wall")
                        else:
                            self.tiles[h][w].updateState("tile")
        
                    
    def updateAlgorithm(self, newAlgorithm):
        for button in self.algButtons:
            button.highlightFalse()
            
        newAlgorithm.highlightTrue()
        self.algorithmSelected = newAlgorithm.text
            
        

    def clickUp(self): 
        self.leftBeingClicked = False
        self.rightBeingClicked = False
        self.originDragged = False
        self.targetDragged = False
        
    def defineAlgorithm(self):
        # the map is not solved
        self.solved = False
        
        # if this is not the first time running an algorithm we have to clean all non wall / tile tiles
        self.removePathGrid()
        
        originPos = self.pixelsToGrid(*self.originTile.getPosition())
        targetPos = self.pixelsToGrid(*self.targetTile.getPosition())
        
        if self.algorithmSelected == "Breadth FS":
            self.algorithm = BFS(originPos, targetPos, self.getGrid())
            
        elif self.algorithmSelected == "Depth FS":
            self.algorithm = DFS(originPos, targetPos, self.getGrid())
        
        elif self.algorithmSelected == "Greedy FS":
            self.algorithm = GFS(originPos, targetPos, self.getGrid())
            
        elif self.algorithmSelected == "A-Star":
            self.algorithm = AStar(originPos, targetPos, self.getGrid())
    
    def removePathGrid(self):
        for row in self.tiles:
            for tile in row:
                tmp = tile.getState()
                if tmp != "wall" and tmp != "origin" and tmp != "target":
                    tile.updateState("tile")
    
    def getGrid(self):
        grid = []
    
        for row in self.tiles:
            boolRow = []
            for tile in row:
                
                if tile.getState() == "wall":
                    boolRow.append(True)
                else: 
                    boolRow.append(False)
                    
            grid.append(boolRow)
        
        return grid
    
    def updateTilesState(self, coords, state):
        for coord in coords:
            (x, y) = coord
            if self.tiles[y][x] != self.originTile and self.tiles[y][x] != self.targetTile:
                self.tiles[y][x].updateState(state)
        
    def pixelsToGrid(self, x, y):
        return (floor(x / self.TILE_W), floor((y - self.Y_OFFSET) / self.TILE_W))
