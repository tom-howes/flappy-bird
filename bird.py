import pygame

birdimage = 'images/bird2.png'

class Bird(pygame.sprite.Sprite):
    def __init__(self, horizontal, vertical):
        
        super().__init__()
        self.image = birdimage
        self.mask = pygame.mask.from_surface(self.image)

        self.x = horizontal
        self.y = vertical
        self.velocity = 0
        self.height = self.y
    
    def flap(self):

        self.velocity = -10.5
        self.height = self.y
    
    def move(self):

        self.y = self.y + self.velocity

    def get_mask(self):

        return pygame.mask.from_surface(self.image)
