import pygame
import pipes
import bird
import os
import neat
from operator import attrgetter

pygame.init()

WIDTH = 800
HEIGHT = 600
TITLE = "Flappy Bird NEAT"
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))
clock = pygame.time.Clock()


class Camera:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y

#camera = Camera(0, 0)
speed = 5
camera = Camera(0, 0)
#pipes.init(screen)
#test_bird = bird.bird(screen, camera)

def colides(bird):
    for pipe in pipes.pipes:
        if pipe.xpos - camera.x <= 50 + bird.rad and pipe.xpos - camera.x + pipe.width >= 50 - bird.rad:
            if bird.ypos + bird.rad> pipe.ypos_gap + pipe.gap_size / 2 or bird.ypos - bird.rad < pipe.ypos_gap - pipe.gap_size /2:
                return True
            else:
                return False
        if bird.ypos + bird.rad > HEIGHT or bird.ypos - bird.rad < 0:
            return True

def find_closest_pipe():
    pipe_min_xpos = min(pipes.pipes, key = attrgetter('xpos'))
    if pipe_min_xpos.xpos < camera.x + 50:
        closest_pipe = pipes.pipes[pipes.pipes.index(pipe_min_xpos) + 1]
    else:
        closest_pipe = pipe_min_xpos
    
    return closest_pipe

def update(b, closest_pipe, human_control):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('quiting')
            quit()
            return False
        if human_control:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    b.jump()
    
    b.update(closest_pipe)
    if colides(b):
        b.genome.fitness -= 200  
        b.color = (255, 0, 0)
        return False
    else:
        b.color = (0, 0, 0)
        return True

#idef render(b):
#    screen.blit(background, (0,0))
#    pipes.render(camera)
#    b.render()
#    pygame.display.flip()

def play_game(genomes, config):
    print('new gen')
    birds = []
    camera.x = 0
    pipes.init(screen)
    render_all = True
    for genome_id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        global bird
        genome.fitness = 0
        birds.append(bird.bird(screen, camera, network, genome))    
    running = True    
    while running:
        clock.tick(FPS)
        screen.blit(background, (0,0))
        #print('-----------------------------------------------------')
        camera.x += speed
        pipes.update(screen, camera)
        closest_pipe = find_closest_pipe()
        pipes.render(camera)
        for b in birds:
            #print('bird:')
            alive = update(b, closest_pipe, False)
            if render_all:
                b.render()
            if not alive:
                birds.remove(b)
        if len(birds) == 0:
            running = False
        if not render_all and running:
            b_best = max(birds, key = attrgetter('genome.fitness'))
            b_best.render()
        pygame.display.flip()
def run_neat(config_file):
    # Load configuration. 
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    #Run for up to 300 generations.
    winner = p.run(play_game, 300)



if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run_neat(config_path)
