import pygame

birdimage = 'images/bird2.png'
MAX_VELOCITY = 5
class Bird(pygame.sprite.Sprite):
    def __init__(self, horizontal, vertical):

        super().__init__()
        self.image = pygame.image.load(birdimage)
        self.mask = pygame.mask.from_surface(self.image)

        self.x = horizontal
        self.y = vertical
        self.velocity = MAX_VELOCITY
        self.height = self.y
        self.flapped = False
    
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
    
    def flap(self):

        self.velocity = -10.5
        self.height = self.y
    
    def move(self):
        self.y = self.y + self.velocity
        if self.velocity <= MAX_VELOCITY:
            self.velocity += 1.5
        else:
            self.velocity = MAX_VELOCITY

    def get_mask(self):

        return pygame.mask.from_surface(self.image)
