import pygame
from math import floor

class Button:
    def __init__(self, x, y, text, font, colorPalette):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.colorPalette = colorPalette
        
        self.padding = 10
        self.yOff = floor(self.padding * 2 / 3) # pygame kind of gives more space to the y axis
        
        self.renderedText = self.font.render(self.text, True, colorPalette["DARKBLUE"])
        self.rect = pygame.Rect(
            self.x - self.padding, 
            self.y - self.padding + self.yOff, 
            self.font.size(self.text)[0] + self.padding * 2, 
            self.font.size(self.text)[1] + self.padding * 2 - self.yOff * 2
            )
        
        self.highlight = False
        
    def draw(self, screen):
        if self.highlight:
            pygame.draw.rect(screen, self.colorPalette["BLUE"], self.rect)
        
        screen.blit(self.renderedText, (self.x, self.y))
    
    def clicked(self, x, y):
        return self.rect.collidepoint(x, y)

    def highlightTrue(self):
        self.highlight = True

    def highlightFalse(self):
        self.highlight = False