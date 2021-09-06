from pygame import Rect

class Tile:
    def __init__(self, x, y, side, lineOffset):
        self.x = x
        self.y = y
        self.side = side
        self.lineOffset = lineOffset
        
        # state can be:
            # tile -> when the state is tile it is not drawn since the background is already tile color
            # wall
            # explored
            # path
            # current
            # target
            # origin
        self.state = "tile"

    def getPosition(self):
        return (self.x, self.y)
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getRect(self):
        return Rect(
            self.x + self.lineOffset + 1, 
            self.y + self.lineOffset + 1, 
            self.side - self.lineOffset * 2 - 1, 
            self.side - self.lineOffset * 2 - 1,
            )

    def updateState(self, state):
        self.state = state
    
    def getState(self):
        return self.state

    def wasItClicked(self, mouseX, mouseY):
        if self.x < mouseX < self.x + self.side and self.y < mouseY < self.y + self.side:
            return True