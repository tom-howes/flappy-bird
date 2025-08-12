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

# Home screen initialization

# pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
elevation = WINDOW_HEIGHT
fps = 32
fps_clock = pygame.time.Clock()
pygame.font.init()

# images / text
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
ldb_button = pygame.image.load("images/ldb-button.png").convert_alpha()
ldb_button_rect = ldb_button.get_rect()

# Leaderboard initialization

leaderboard_frame = pygame.image.load("images/test.png")
leaderboard_rect = leaderboard_frame.get_rect()
leaderboard_rect.center = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
back_button = pygame.image.load("images/back-button.png").convert_alpha()
back_button_rect = back_button.get_rect()
delete_closed = pygame.image.load("images/trash_closed.png").convert_alpha()
delete_open = pygame.image.load("images/trash_open.png").convert_alpha()
delete_rect = delete_closed.get_rect()
delete_rect.center = WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50

# Confimation screen initalization
large_font = pygame.font.SysFont(None, 40)
confirm_text = large_font.render(' Are you sure you want\nto reset the leaderboard?', True, 'BLACK')
confirm_text_rect = confirm_text.get_rect()
confirm_text_rect.center = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4
yes_button = pygame.image.load("images/tick.png").convert_alpha()
no_button = pygame.image.load("images/cross.png").convert_alpha()
yes_button_rect = yes_button.get_rect()
yes_button_rect.center = WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2
no_button_rect = no_button.get_rect()
no_button_rect.center = WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2

# Game over screen initialization
game_over = pygame.image.load("images/game_over.png").convert_alpha()
game_over_rect = game_over.get_rect()
game_over_rect.center = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3
home_button = pygame.image.load("images/home.png").convert_alpha()
home_button_rect = home_button.get_rect()
home_button_rect.x, home_button_rect.y = back_button_rect.x, (WINDOW_HEIGHT - home_button.get_height())



def draw_game_state(bird, pipes, score):
    """ Blits each frame of ongoing game to window

        bird -- bird object
        pipes -- array of pipe objects
        score -- player's current score
    """

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

    for num in numbers:
        window.blit(score_images[num], (x_offset, WINDOW_WIDTH * 0.02))
        x_offset += score_images[num].get_width()

def check_button_hover(button_rect, button, x, y):
    """ Returns true if mouse is over a given button

        button_rect -- pygame rect of button img
        button -- clickable menu button
        x -- mouse x pos
        y -- mouse y pos
    """
    if button_rect.x < x < button_rect.x + button.get_width():
        if button_rect.y < y < button_rect.y + button.get_height():
            return True
    
    return False

def draw_leaderboard(leaderboard):
    """ Draws a new screen with the current leaderboard, a back button and a delete button

        leaderboard -- current leaderboard object
    """
    ldb = leaderboard.get_leaderboard()   
    while True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_BACKSPACE):
                return
            if event.type == MOUSEBUTTONDOWN:
                if check_button_hover(back_button_rect, back_button, x, y):
                    return
                if check_button_hover(delete_rect, delete_open, x, y):
                    if confirm():
                        # Reverts leaderboard to blank template
                        leaderboard.reset()
                    return    
        
        window.blit(background, (0, 0))
        window.blit(leaderboard_frame, leaderboard_rect)
        window.blit(back_button, back_button_rect)

        # Animation for trash can opening on hover over delete button
        if check_button_hover(delete_rect, delete_closed, x, y):
            window.blit(delete_open, delete_rect)
        else:
            window.blit(delete_closed, delete_rect)

        y = 143

        # Blits player name and score onto leaderboard frame
        for player in ldb:
            x = 195
            name = font.render(player['name'], True, 'WHITE')
            score = font.render(player['score'], True, 'WHITE')
            window.blit(name, (x, y))
            x += 255
            score_rect = score.get_rect()
            score_rect.topright = (x, y)
            window.blit(score, score_rect)
            y += 52
        pygame.display.update()

        fps_clock.tick(fps)

def draw_game_over(score, leaderboard):
    """ Draws a Game Over screen that displays player score and allows player to go to home screen or leaderboard

        score -- current player score to be displayed
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Go to leaderboard screen
                if check_button_hover(ldb_button_rect, ldb_button, x, y):
                    draw_leaderboard(leaderboard)
                # Returns to home screen
                if check_button_hover(home_button_rect, home_button, x, y):
                    main()

        # Background, Game Over text and player score     
        window.blit(background, (0, 0))
        window.blit(game_over, game_over_rect)
        score_text = large_font.render(f'Your Score : {score}', True, 'Black')
        score_text_rect = score_text.get_rect()
        score_text_rect.center = WINDOW_WIDTH / 2,  (WINDOW_HEIGHT / 1.3)
        window.blit(score_text, score_text_rect)
        window.blit(ldb_button, ldb_button_rect)
        window.blit(home_button, home_button_rect)
        pygame.display.update()
    
        fps_clock.tick(fps)

def confirm():
    """ Confirmation screen to make sure player wants to reset leaderboard
    """
    while True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                # Delete leaderboard
                if check_button_hover(yes_button_rect, yes_button, x, y):
                    return True
                # Return to prev screen
                if check_button_hover(no_button_rect, no_button, x, y):
                    return False
        window.blit(background, (0, 0))
        window.blit(confirm_text, confirm_text_rect)
        window.blit(yes_button, yes_button_rect)
        window.blit(no_button, no_button_rect)
        
        pygame.display.update()
        fps_clock.tick(fps)

def death_animation(bird, pipes, score):
    """ When a collision occurs, flip the bird upside down and fall out of the sky

        bird -- bird object
        pipes -- array of pipes
        score -- current player score
    """
    window.blit(background, (0, 0))

    # Draw pipes stationary
    for pipe in pipes:
        pipe.stop()
        pipe.draw(window)
    bird.fall()
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
    
    pygame.display.update()

    fps_clock.tick(fps)

def flappygame(leaderboard):
    """  Main game loop that begins after player enters name and initiates game

        leaderboard -- leaderboard object that keeps track of top scores
    """

    # Init bird and pipe start positions, score set to 0
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

        for pipe in pipes:
            pipe.move()
            # Check for collisions
            if pipe.collision(bird, window) or bird.check_bounds(WINDOW_HEIGHT):
                # Play death animation only if bird hits pipe
                while not bird.check_bounds(WINDOW_HEIGHT):
                    death_animation(bird, pipes, score)
                leaderboard.add_current_score(score)
                leaderboard.update()
                draw_game_over(score, leaderboard)
                return
            # Remove pipes that hit end of screen
            if pipe.x + pipe.top_pipe.get_width() < 5:
                pipes.remove(pipe)
            
            # Increment score if pipe passed
            if not pipe.passed and pipe.x + (pipe.top_pipe.get_width() / 2) < bird.x:
                pipe.passed = True
                score += 1
                pipes.append(Pipe(WINDOW_WIDTH, score))
            
                 
        # Blits current image / score status to screen
        draw_game_state(bird, pipes, score) 

        
        # Refreshing game window and displaying the score
        pygame.display.update()

        # Set FPS
        fps_clock.tick(fps)
        

def main():
    """ Main (home screen) function that initiates the flappy bird instance
    """

    pygame.display.set_caption('Flappy Bird')
    
    # Terminal output
    print("WELCOME TO TOM'S FLAPPY BIRD")
    print("Press space or enter to start the game")

    # Used by blinking text
    show_text = True
    
    player_name = ""
    name_colour = pygame.Color('White')
    leaderboard = Leaderboard(score_file, "")

    while True:       
        for event in pygame.event.get():

            # Exit application on user pressing ESC or clicking X
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Start game on user pressing SPACE or UP
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_name != "":
                    leaderboard.set_player(player_name)
                    flappygame(leaderboard)
                else:
                    name_colour = (255, 0, 0)

            # Maintain starting image if no user action
            if event.type == BLINK_EVENT:
                show_text = not show_text
            
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if check_button_hover(ldb_button_rect, ldb_button, x, y):
                    draw_leaderboard(leaderboard)
            
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

            window.blit(ldb_button, (0, 0))

            if player_name == "":
                window.blit(name_surface, (input_rect.x + 5, input_rect.y + 8))

            # Refreshes screen
            pygame.display.update()

            # Set framerate
            fps_clock.tick(fps)

if __name__ == "__main__":
    main()