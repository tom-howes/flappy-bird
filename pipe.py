import pygame
import random
MAX_HEIGHT = 100
START_VELOCITY = 5

class Pipe():

    def __init__(self, x, score, slowed):
        """ Initialises a pipe object with a random height
        """
        self.x = x

        self.top = 0
        pipe_image = pygame.image.load("images/new_pipe_biggest.png").convert_alpha()
        
        # Top pipe is flipped bottom pipe
        self.top_pipe = pygame.transform.flip(pipe_image, False, True)
        self.bottom_pipe = pipe_image
        from flappy import WINDOW_HEIGHT
        self.bottom = WINDOW_HEIGHT - pipe_image.get_height()

        # Pipe speed increments with score in multiples of 5
        self.acceleration = (score // 5)
        self.velocity = START_VELOCITY + self.acceleration

        # Check for slow powerup, reduce velocity
        self.slowed = slowed

        self.passed = False

        self.random_height()

    def random_height(self):
        """ Randomises height of top and bottom pipes between
            0 -- largest gap
            100 -- smallest gap
        """
        self.top -= random.randrange(0, MAX_HEIGHT)
        self.bottom += random.randrange(0, MAX_HEIGHT)

    def move(self):
        """ increments pipe x value by current velocity
        """
        if self.slowed:
            self.x -= (self.velocity * 0.8)
        else:
            self.x -= self.velocity

    def draw(self, window):
        """ blits pipes on window
        """
        window.blit(self.top_pipe, (self.x, self.top))
        window.blit(self.bottom_pipe, (self.x, self.bottom))
    
    def collision(self, object):
        """ Checks if bird/powerup overlaps with bottom pipe or top pipe
            bird -- bird or powerup object
            If masks overlap collision occurs - Return True
        """
        object_mask = object.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)

        top_offset = (self.x - object.x, self.top - object.y)
        bottom_offset = (self.x - object.x, self.bottom - object.y)

        b_coll = object_mask.overlap(bottom_mask, bottom_offset)
        t_coll = object_mask.overlap(top_mask, top_offset)

        if b_coll or t_coll:
            return True
        
        return False
    
    def print_pos(self):
        """ Used for debugging
        """
        print("x: ", self.x)
    
    def stop(self):
        """ Invoked when collision has occurred for bird falling animation
        """
        self.velocity = 0
        self.acceleration = 0

    def slow_down(self):
        self.slowed = True
    
    def speed_up(self):
        self.slowed = False