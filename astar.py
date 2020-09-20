import pygame, sys, math

# Color constants
WHITE = 255, 255, 255
BLACK = 0, 0, 0
LIGHT_BLUE = 25, 120, 250
RED = 255, 0, 0
GREEN = 0, 255, 0

rows, cols = 50, 50
tile_size = 12

window_width, window_height = cols*tile_size, rows*tile_size

pygame.init()
win = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

class Spot:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        
    def show(self, win, color):
        pygame.draw.rect(win, color, (self.x*tile_size, self.y*tile_size, tile_size-1, tile_size-1))
    
    def add_neighbors(self, grid):
        x_offset = (1,  1,  1,  0, 0, -1, -1, -1)
        y_offset = (-1, 0,  1, -1, 1, -1,  0,  1)

        for x, y in zip(x_offset, y_offset):  # For each neighbor
            if self.x+x > -1 and self.y+y > -1 and self.x+x < cols and self.y+y < rows:  # If it's in bounds
                self.neighbors.append(grid[self.x+x][self.y+y])  # Add it to it's neighbor list

# Put or remove walls
def clickWall(pos, state):
    tile = grid[pos[0] // tile_size][pos[1] // tile_size]
    if tile not in (start, end):
        tile.wall = state
            
def heuristics(a, b):
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)

# Fill the grid with a 2d array of Spots (rows*cols)
grid = [[Spot(x, z) for z in range(rows)] for x in range(cols)]

# Calculate each neighbor count in the grid 
for column in grid:
    for cell in column:
        cell.add_neighbors(grid)

# Put the start in the top left corner and end 3/4th in
start = grid[0][0]
end = grid[cols - cols//4][rows - rows//4]

openSet = [start]
closeSet = []
path = []

def main():

    processing = False

    while True:
        '''
        Event handler for drawing the obstacles and starting the algorithm
        '''
        for event in pygame.event.get():  # All events (mouse moving, button clicks, mouse clicks etc)
            if event.type == pygame.QUIT:  # If they try to close the window
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If they press the mouse (any button)
                if event.button in (1, 3):  # And it's a left or right click
                    clickWall(pygame.mouse.get_pos(), event.button==1)  # Click a wall with either (True as a left click or False as not a left click (a right click)

            elif event.type == pygame.MOUSEMOTION:
                # event.buttons is a tuple of (x, y, z) e.g. (1, 0, 0) if they're holding a button, x = left click, y = middle and z = right click
                if event.buttons[0] or event.buttons[2]:  # If they're holding left or right click while dragging the mouse
                    clickWall(pygame.mouse.get_pos(), event.buttons[0])  # if the left click is being held, send True, else False (Right click)
                    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                processing = True

        '''
        When we begin (Return)
        '''
        if processing:
            if len(openSet) > 0:
                current = min(openSet, key = lambda x: x.f)

                if current == end:  # If we've found the end
                    temp = current
                    while temp.prev:  # Working backwards from the end
                        path.append(temp.prev)
                        temp = temp.prev

                    # Once we've tracked from the end to the start, and built the path
                    processing = False
                    print("Solution found")

                if processing:
                    openSet.remove(current)
                    closeSet.append(current)
                    # Move the current tile from the open set to the closed set

                    for neighbor in current.neighbors:
                        if neighbor not in closeSet and not neighbor.wall:
                                
                            tempG = current.g + 1

                            newPath = False
                            if neighbor in openSet:
                                if tempG < neighbor.g:
                                    neighbor.g = tempG
                                    newPath = True
                            else:
                                neighbor.g = tempG
                                newPath = True
                                openSet.append(neighbor)
                            
                            if newPath:
                                neighbor.h = heuristics(neighbor, end)
                                neighbor.f = neighbor.g + neighbor.h
                                neighbor.prev = current

            else:
                print("No Solution!\n-> There was no possible solution")
                break

        '''
        Drawing the results
        '''
        for column in grid:
            for spot in column:

                if spot.wall:
                    spot.show(win, BLACK)
                elif spot == end:
                    spot.show(win, LIGHT_BLUE)
                elif spot in path and not processing:
                    spot.show(win, LIGHT_BLUE)
                elif spot in closeSet:
                    spot.show(win, RED)
                elif spot in openSet:
                    spot.show(win, GREEN)
                else:
                    spot.show(win, WHITE)
                    
        pygame.display.flip()

main()
