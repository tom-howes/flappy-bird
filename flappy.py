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
birdimage = 'images/bird2.png'
background = 'images/background.jpg'

def create_pipe():
    pipe_gap = WINDOW_HEIGHT / 3
    pipe_height = game_images['pipe'][0].get_height()

    # Random pipe height generation
    y2 = pipe_gap + random.randrange(0, int(WINDOW_HEIGHT - 1.2 * pipe_gap))
    pipe_x = WINDOW_WIDTH + 10
    y1 = pipe_height - y2 + pipe_gap
    pipe = [
        # Top pipe
        {'x': pipe_x, 'y': -y1},
        # Bottom pipe
        {'x': pipe_x, 'y': y2}
    ]
    return pipe

def is_game_over(horizontal, vertical, top_pipes, bottom_pipes):

    # Check if bird hits top or bottom
    if vertical < 0 or vertical > elevation - 25:
        return True
    
    # Check if bird hits bottom pipe
    for pipe in bottom_pipes:
        pipe_height = game_images['pipe'][0].get_height()
        if vertical < pipe_height + pipe['y'] and \
        abs(horizontal - pipe['x']) < game_images['pipe'][0].get_width():
            return True
    
    # Check if bird hits top pipe
    for pipe in top_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and \
        abs(horizontal - pipe['x']) < game_images['pipe'][0].get_width():
            return True
    
    return False

def flappygame():
    score = 0
    horizontal = int(WINDOW_HEIGHT/5)
    vertical = int(WINDOW_WIDTH/2)
    temp_height = 100

    # Generate two pipes
    first_pipe = create_pipe()
    second_pipe = create_pipe()

    # List of top pipes (pipes facing down)
    top_pipes = [
        {'x' : WINDOW_WIDTH + 300 - temp_height,
         'y' : first_pipe[1]['y']},
         {'x' : WINDOW_WIDTH + 300 - temp_height + (WINDOW_WIDTH/2),
          'y' : second_pipe[1]['y']}
    ]

    # List of bottom pipes (pipes facing up)
    bottom_pipes = [
        {'x' : WINDOW_WIDTH + 300 - temp_height,
         'y' : first_pipe[0]['y']},
         {'x' : WINDOW_WIDTH + 200 - temp_height + (WINDOW_WIDTH / 2),
          'y' : second_pipe[1]['y']}
    ]

    pipe_vel_x = -4 # pipe velocity along x axis

    # Bird movement
    bird_velocity_y = -9
    max_bird_velocity_y = 10 # fastest it can rise
    min_bird_velocity_y = -8 # fastest it can fall
    bird_acceleration_y = 1 # Acceleration of bird

    bird_flap_velocity = -8 # velocity while flapping

    bird_flapped = False

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True
        
        # Exits function if game is over
        game_over = is_game_over(horizontal, vertical, top_pipes, bottom_pipes)
        if game_over:
            return
        
        # Check for score
        player_mid_pos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in bottom_pipes:
            pipe_mid_pos = pipe['x'] + game_images['pipe'][0].get_width()/2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                print(f"Your score is {score}")
        
        if bird_velocity_y < max_bird_velocity_y and not bird_flapped:
            bird_velocity_y += bird_acceleration_y
        
        if bird_flapped:
            bird_flapped = False
        
        player_height = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - player_height)

        # Move pipes to the left
        for top_pipe, bottom_pipe in zip(bottom_pipes, top_pipes):
            bottom_pipe['x'] += pipe_vel_x
            top_pipe['x'] += pipe_vel_x
        
        # Add new pipe when first is about to hit the left side of the window
        if 0 < bottom_pipes[0]['x'] < 5:
            new_pipe = create_pipe()
            bottom_pipes.append(new_pipe[0])
            top_pipes.append(new_pipe[1])

        # Remove pipe if its off the screen

        if bottom_pipes[0]['x'] < -game_images['pipe'][0].get_width():
            top_pipes.pop(0)
            bottom_pipes.pop(0)
        
        # blit game images

        window.blit(game_images['background'], (0, 0))
        for bottom_pipe, top_pipe in zip(bottom_pipes, top_pipes):
            window.blit(game_images['pipe'][0], (bottom_pipe['x'], bottom_pipe['y']))
            window.blit(game_images['pipe'][1], (top_pipe['x'], top_pipe['y']))
        
        window.blit(game_images['flappybird'], (horizontal, vertical))

        # Fetching digits of score
        numbers = [int(x) for x in list(str(score))]
        width = 0

        # Finding width of score images from numbers
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        
        x_offset = (WINDOW_WIDTH - width)/1.1

        # Blitting images on the window
        for num in numbers:
            window.blit(game_images['scoreimages'][num], (x_offset, WINDOW_WIDTH * 0.02))
            x_offset += game_images['scoreimages'][num].get_width()
        
        # Refreshing game window and displaying the score
        pygame.display.update()

        # Set FPS
        fps_clock.tick(fps)
        

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
                    flappygame()

                # Maintain starting image if no user action
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'], (horizontal, vertical))

                    # Refreshes screen
                    pygame.display.update()

                    # Set framerate
                    fps_clock.tick(fps)