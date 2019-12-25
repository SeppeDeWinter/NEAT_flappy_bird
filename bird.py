import pygame
pygame.init()

class bird:

    def __init__(self, Screen, Camera, brain, Genome):
        w, h = Screen.get_size()
        self.screen = Screen
        self.camera = Camera
        self.ypos = h/2
        self.xpos = Camera.x
        self.yvel = 0
        self.color = (0, 0, 0)
        self.rad = 20
        self.network = brain
        self.genome = Genome    
    def jump(self):
        self.yvel = -4

    def update(self, closest_pipe):
        self.yvel = self.yvel + 0.2
        self.ypos = self.ypos + self.yvel
        self.xpos = self.camera.x
        output_net = self.network.activate((self.ypos - closest_pipe.ypos_gap, abs(self.xpos - closest_pipe.xpos + closest_pipe.width), self.yvel, closest_pipe.gap_size))
        self.genome.fitness = self.xpos
        self.genome.fitness += 0.3
        #print(self.yvel)
        if output_net[0] > 0.5:
            self.jump()


    def render(self):
        pygame.draw.circle(self.screen, self.color, (int(50), int(self.ypos)), self.rad)

