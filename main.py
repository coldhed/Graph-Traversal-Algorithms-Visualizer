import pygame
from Grid import Grid
from math import floor

pygame.init()

# nothing is hard-coded so that you can change the tile_W (as long as it is a divisor of width and height)
WIDTH = 1000
HEIGHT = 600
MENU_HEIGHT = 200
TILE_W = 25
LINE_WIDTH = 1 # should be an odd number so that it all lines up 
RECT_OFF = floor(LINE_WIDTH / 2) # offset due to the line's width
TEXT_SIZE = 42
FPS_SOLVE = 15

# color palette -> depends on tiles state
colorPalette = {
    "GRAY" : (205, 211, 213),  # tile
    "BLUE" : (117, 184, 200),  # seen
    "MINT" : (119, 203, 185),  # path
    "ORANGE" : (255, 153, 51), # current
    "DARKBLUE" : (10, 16, 69), # wall
    "RED" : (238, 99, 82),     # target
    "GREEN" : (21, 97, 109),   # origin
}


screen = pygame.display.set_mode([WIDTH, HEIGHT + MENU_HEIGHT])
pygame.display.set_caption('Graph Traversal Algorithms Visualizer')
clock = pygame.time.Clock()

def main():    
    # Run until the user asks to quit
    running = True
    
    # gamestate
        # can be:
        # - draw
        # - solve
        #   -> when it finishes solving it returns to draw state

    gameState = "draw"

    grid = Grid(WIDTH, HEIGHT, TILE_W, colorPalette, LINE_WIDTH, MENU_HEIGHT, TEXT_SIZE)
    
    while running:
        # click game while solving so algorithms can be visualized
        if gameState == "solve":
            clock.tick(grid.FPS)
        
        #   PYGAME EVENTS
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                running = False
               
            # key presses
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and gameState == "draw":
                    gameState = "solve"
                    grid.defineAlgorithm()

            # mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                left, _, _ = pygame.mouse.get_pressed()
                grid.clickDown(*pygame.mouse.get_pos(), left, gameState)
            
            if event.type == pygame.MOUSEBUTTONUP:
                    grid.clickUp()
                
        #           U P D A T E
        grid.update(gameState)   
        if grid.solved:
            gameState = "draw"
        
        #            D R A W  
        screen.fill(colorPalette["GRAY"]) # background
        grid.draw(screen)
        
        # update the display
        pygame.display.flip()

    pygame.quit()
             
main() 