import random
import sys
import pygame
from leaderboard import Leaderboard
from pygame.locals import *
from bird import Bird
from pipe import Pipe
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 499

score_file = "scores/leaderboard_current.json"

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
title = pygame.image.load('images/Title_text.png').convert_alpha()
title_rect = title.get_rect()
title_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50)
pygame.font.init()
font = pygame.font.SysFont(None, 24)
text = font.render('Press SPACE or UP to play!', True, 'WHITE')
text_rect = text.get_rect()
text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 190)
BLINK_EVENT = pygame.event.custom_type()
pygame.time.set_timer(BLINK_EVENT, 500)
show_text = True

player_name = ''
enter_name = 'Enter Name...'
input_rect = pygame.Rect(WINDOW_WIDTH / 2 - 70, WINDOW_HEIGHT / 2 + 120, 140, 32)
colour = pygame.Color('White')
name_colour = pygame.Color('White')


def draw_game_state(bird, pipes, score):
    window.blit(background, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    
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

def flappygame(player_name):
    leaderboard = Leaderboard(score_file, player_name)
    score = 0
    horizontal = int(WINDOW_HEIGHT/5)
    vertical = int(WINDOW_WIDTH/2)

    pipes = [Pipe(WINDOW_WIDTH, score)]
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

        for pipe in pipes:
            pipe.move()
            if pipe.collision(bird, window) or bird.check_bounds(WINDOW_HEIGHT):
                leaderboard.add_current_score(score)
                leaderboard.update()
                print("game over!")
                return
            if pipe.x + pipe.top_pipe.get_width() < 5:
                remove.append(pipe)
            
            if not pipe.passed and pipe.x + (pipe.top_pipe.get_width() / 2) < bird.x:
                pipe.passed = True
                score += 1
                pipes.append(Pipe(WINDOW_WIDTH, score))
            
            for r in remove:
                pipes.remove(r)
                 
        
        draw_game_state(bird, pipes, score) 

        
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
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    if player_name != "":
                        flappygame(player_name)
                    else:
                        name_colour = (255, 0, 0)

                # Maintain starting image if no user action
                if event.type == BLINK_EVENT:
                    show_text = not show_text
                
                if event.type == KEYDOWN and (event.key != K_SPACE and event.key != K_UP):
                    if event.unicode.isalnum() and len(player_name) < 9:
                        player_name += event.unicode
                
                if event.type == KEYDOWN and (event.key == K_BACKSPACE):
                    player_name = player_name[:-1]

                window.blit(background, (0, 0))
                window.blit(title, title_rect)
                if show_text:
                    window.blit(text, text_rect)

                pygame.draw.rect(window, colour, input_rect, 2)
                
                text_surface = font.render(player_name, True, (255, 255, 255))
                name_surface = font.render(enter_name, True, name_colour)
                name_surface.set_alpha(128)
                window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

                if player_name == "":
                    window.blit(name_surface, (input_rect.x + 5, input_rect.y + 5))

                # Refreshes screen
                pygame.display.update()

                # Set framerate
                fps_clock.tick(fps)