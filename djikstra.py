"""Djikstra's Path Finding"""

import pygame, sys, random, math
from collections import deque
from tkinter import messagebox, Tk

size = (width, height) = 640, 480
pygame.init()

win = pygame.display.set_mode(size)
pygame.display.set_caption("Dijktdtra's Path Finding")
clock = pygame.time.Clock()

cols, rows = 64, 48

w = width//cols
h = height//rows

grid = []
queue, visited = deque(), []
path = []

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        if (i+j)%7 == 0:
            self.wall == True
        # if random.randint(0, 100) < 20:
        #     self.wall = True
        
    def show(self, win, col, shape= 1):
        if self.wall == True:
            col = (0, 0, 0)
        if shape == 1:
            pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
        else:
            pygame.draw.circle(win, col, (self.x*w+w//2, self.y*h+h//2), w//3)
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        #Add Diagonals
        # if self.x < cols - 1 and self.y < rows - 1:
        #     self.neighbors.append(grid[self.x+1][self.y+1])
        # if self.x < cols - 1 and self.y > 0:
        #     self.neighbors.append(grid[self.x+1][self.y-1])
        # if self.x > 0 and self.y < rows - 1:
        #     self.neighbors.append(grid[self.x-1][self.y+1])
        # if self.x > 0 and self.y > 0:
        #     self.neighbors.append(grid[self.x-1][self.y-1])


def clickWall(pos, state):
    i = pos[0] // w
    j = pos[1] // h
    grid[i][j].wall = state

def place(pos):
    i = pos[0] // w
    j = pos[1] // h
    return w, h

for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

    
start = grid[0][0]
end = grid[cols - cols//2][rows - cols//4]
start.wall = False
end.wall = False

queue.append(start)
start.visited = True

def main():
    flag = False
    noflag = True
    startflag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):  
                    clickWall(pygame.mouse.get_pos(), event.button==1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:
                    clickWall(pygame.mouse.get_pos(), event.buttons[0])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True

        if startflag:
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev 
                    if not flag:
                        flag = True
                        print("Done")
                    elif flag:
                        continue
                if flag == False:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There was no solution" )
                    noflag = False
                else:
                    continue


        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, (44, 62, 80))
                if spot in path:
                    spot.show(win, (46, 204, 113))
                    spot.show(win, (192, 57, 43), 0)
                elif spot.visited:
                    spot.show(win, (39, 174, 96))
                if spot in queue and not flag:
                    spot.show(win, (44, 62, 80))
                    spot.show(win, (39, 174, 96), 0)
                if spot == start:
                    spot.show(win, (0, 255, 200))
                if spot == end:
                    spot.show(win, (0, 120, 255))
                
                
        pygame.display.flip()


main()
