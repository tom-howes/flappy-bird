import pygame
import random

gap = 200
velocity = 5

class Pipe():

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        pipe_image = pygame.image.load("images/new_pipe_biggest.png").convert_alpha()
        
        self.top_pipe = pygame.transform.flip(pipe_image, False, True)
        self.bottom_pipe = pipe_image

        self.passed = False

        self.random_height()

    def random_height(self):

        self.height = random.randrange(50, 450)
        self.top = self.height - self.top_pipe.get_height()
        self.bottom = self.height + gap
        
    def move(self):
        self.x -= velocity

    def draw(self, window):
        window.blit(self.top_pipe, (self.x, self.top))
        window.blit(self.bottom_pipe, (self.x, self.bottom))
    
    def collision(self, bird, window):

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)

        top_offset = (self.x - bird.x, self.top - bird.y)
        bottom_offset = (self.x - bird.x, self.bottom - bird.y)

        b_coll = bird_mask.overlap(bottom_mask, bottom_offset)
        t_coll = bird_mask.overlap(top_mask, top_offset)

        if b_coll or t_coll:
            return True
        
        return False
    
    def print_pos(self):
        print("x: ", self.x, "y: ", self.height)