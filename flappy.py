import random
import sys
import pygame
from pygame.locals import *
from bird import Bird
from pipe import Pipe
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 499

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
elevation = WINDOW_HEIGHT
fps = 32
background = pygame.image.load('images/background.jpg')
score_images = [pygame.image.load('images/0.jpg').convert_alpha(),
                pygame.image.load('images/1.jpg').convert_alpha(),
                pygame.image.load('images/2.jpg').convert_alpha(),
                pygame.image.load('images/3.jpg').convert_alpha(),
                pygame.image.load('images/4.jpg').convert_alpha(),
                pygame.image.load('images/5.jpg').convert_alpha(),
                pygame.image.load('images/6.jpg').convert_alpha(),
                pygame.image.load('images/7.jpg').convert_alpha(),
                pygame.image.load('images/8.jpg').convert_alpha(),
                pygame.image.load('images/9.jpg').convert_alpha()]

# def create_pipe():
#     pipe_gap = WINDOW_HEIGHT / 3
#     pipe_height = game_images['pipe'][0].get_height()

#     # Random pipe height generation
#     y2 = 0 # + random.randrange(0, int(WINDOW_HEIGHT - 1.2 * pipe_gap))
#     pipe_x = WINDOW_WIDTH + 10
#     y1 = WINDOW_HEIGHT - pipe_height
#     pipe = [
#         # Bottom pipe
#         {'x': pipe_x, 'y': y1},
#         # Top pipe
#         {'x': pipe_x, 'y': y2}
#     ]
#     return pipe

# def is_game_over(horizontal, vertical, top_pipes, bottom_pipes, bird):
#     # Check if bird hits high or low
#     if vertical < 0 or vertical > WINDOW_HEIGHT - 25:
#         return True
#     pipe_height = game_images['pipe'][0].get_height()
#     pipe_width = game_images['pipe'][0].get_width()
#     # Check if bird hits high pipe
#     for pipe in top_pipes:
#         print("high pipe: ", "x: ", pipe['x'], "y: ", pipe['y'], end=" ")
#         print("horizontal: ", horizontal)
        
#         if vertical < pipe['y'] + pipe_height and \
#         pipe['x'] + 10 < horizontal < pipe['x'] + pipe_width - 10:
#             print("top hit at:", pipe['x'])
#             print(pipe['x'], pipe['y'])
#             return True
    
#     # Check if bird hits high pipe
#     for pipe in bottom_pipes:
#         # print("low pipe: ", "x: ", pipe['x'], "y: ", pipe['y'])
#         pipe_mask = pygame.mask.from_surface(pipe_image)
#         player_mask = pygame.mask.from_surface(birdimage)
#         if pygame.sprite.collide_mask(bird, bird):
#             print("bird collided")
    
#     return False

def flappygame():
    score = 0
    horizontal = int(WINDOW_HEIGHT/5)
    vertical = int(WINDOW_WIDTH/2)

    pipes = [Pipe(WINDOW_WIDTH)]
    bird = Bird(horizontal, vertical)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                bird.flap()
        
        bird.move()
        
        remove = []

        window.blit(background, (0, 0))

        for pipe in pipes:
            pipe.draw(window)
            pipe.move()
            pipe.print_pos()
            if pipe.collision(bird, window):
                print("game over!")
                return
            if pipe.x + pipe.top_pipe.get_width() < 0:
                remove.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                score += 1
                pipes.append(Pipe(WINDOW_WIDTH))
            
            for r in remove:
                pipes.remove(r)
        
        bird.draw(window)

        # Fetching digits of score
        numbers = [int(x) for x in list(str(score))]
        width = 0

        # Finding width of score images from numbers
        for num in numbers:
            width += score_images[num].get_width()
        
        x_offset = (WINDOW_WIDTH - width)/1.1

        # Blitting images on the window
        for num in numbers:
            window.blit(score_images[num], (x_offset, WINDOW_WIDTH * 0.02))
            x_offset += score_images[num].get_width()
        
        # Refreshing game window and displaying the score
        pygame.display.update()

        # Set FPS
        fps_clock.tick(fps)
        

if __name__ == "__main__":

    pygame.init()
    fps_clock = pygame.time.Clock()

    pygame.display.set_caption('Flappy Bird')
    
    print("WELCOME TO TOM'S FLAPPY BIRD")
    print("Press space or enter to start the game")

    while True:
        
        horizontal = int(WINDOW_WIDTH / 5)
        vertical = int(WINDOW_HEIGHT / 2)

        ground = 0
        while True:
            for event in pygame.event.get():

                # Exit application on user pressing ESC or clicking X
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()

                    sys.exit()

                # Start game on user pressing SPACE or UP
                elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    flappygame()

                # Maintain starting image if no user action
                else:
                    window.blit(background, (0, 0))
                    bird = Bird(horizontal, vertical)
                    bird.draw(window)

                    # Refreshes screen
                    pygame.display.update()

                    # Set framerate
                    fps_clock.tick(fps)