import random
import sys
import pygame
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 499

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
elevation = WINDOW_HEIGHT * 0.8
game_images = {}
fps = 32
pipeimage = 'images/pipe.png'
birdimage = 'images/bird.png'
background = 'images/background.jpg'

if __name__ == "__main__":

    pygame.init()
    fps_clock = pygame.time.Clock()

    pygame.display.set_caption('Flappy Bird')

    game_images['scoreimages'] = (
            pygame.image.load('images/0.jpg').convert_alpha(),
            pygame.image.load('images/1.jpg').convert_alpha(),
            pygame.image.load('images/2.jpg').convert_alpha(),
            pygame.image.load('images/3.jpg').convert_alpha(),
            pygame.image.load('images/4.jpg').convert_alpha(),
            pygame.image.load('images/5.jpg').convert_alpha(),
            pygame.image.load('images/6.jpg').convert_alpha(),
            pygame.image.load('images/7.jpg').convert_alpha(),
            pygame.image.load('images/8.jpg').convert_alpha(),
            pygame.image.load('images/9.jpg').convert_alpha()
    )
    game_images['flappybird'] = pygame.image.load(birdimage).convert_alpha()
    game_images['background'] = pygame.image.load(background).convert_alpha()
    game_images['pipe'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
                           pygame.image.load(pipeimage).convert_alpha())
    
    print("WELCOME TO TOM'S FLAPPY BIRD")
    print("Press space or enter to start the game")

    while True:
        
        horizontal = int(WINDOW_WIDTH / 5)
        vertical = int((WINDOW_HEIGHT - game_images['flappybird'].get_height()) / 2)

        ground = 0
        while True:
            for event in pygame.event.get():

                # Exit application on user pressing ESC or clicking X
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()

                    sys.exit()

                # Start game on user pressing SPACE or UP
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    pass

                # Maintain starting image if no user action
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'], (horizontal, vertical))

                    # Refreshes screen
                    pygame.display.update()

                    # Set framerate
                    fps_clock.tick(fps)