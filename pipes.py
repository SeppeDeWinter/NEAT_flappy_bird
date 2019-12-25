import pygame
import random

pygame.init() 

black = (0, 0, 0)

pipes = []
npipe = 4

def init(screen):
    global pipes
    global npipe
    pipes = [] 
    npipe = 4
    w, h = screen.get_size()
    pipes.append(Pipe(screen, 400, random.randint(w/2 - 100, w/2 + 100), random.randint(150, 250)))
    pipes.append(Pipe(screen, 400 + (w/10) * 5, random.randint(w/2 - 100, w/2 + 100), random.randint(150, 250)))
    pipes.append(Pipe(screen, 400 + (w/10) * 10, random.randint(w/2 - 100, w/2 + 100), random.randint(150, 250)))
    pipes.append(Pipe(screen, 400 + (w/10) * 15, random.randint(w/2 - 100, w/2 + 100), random.randint(150, 250)))

def update(screen, camera):
    w, h = screen.get_size()
    for pipe in pipes:
        if pipe.xpos + pipe.width < camera.x:
            global npipe
            pipes.remove(pipe)
            pipes.append(Pipe(screen, 400 + (w/10) * npipe * 5, random.randint(w/2 - 100, w/2 + 100), random.randint(150, 200)))
            npipe = npipe + 1
def render(camera):
    for pipe in pipes:
        pipe.render(camera)

class Pipe:
    def __init__(self, Screen, Xpos, Ypos_gap, Gap_size):
            self.xpos = Xpos
            self.ypos_gap = Ypos_gap
            self.gap_size = Gap_size
            self.screen = Screen
            self.w, self.h = Screen.get_size()
            self.width = self.w / 10

    def render(self, camera):
        pygame.draw.rect(self.screen, black, (self.xpos - camera.x, 0, self.width, self.ypos_gap - self.gap_size / 2))
        pygame.draw.rect(self.screen, black, (self.xpos - camera.x, self.ypos_gap + self.gap_size / 2, self.width, self.h - self.ypos_gap + self.gap_size / 2))
    
