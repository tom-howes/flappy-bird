import pygame
import time

birdimages = [
    'images/bird-dn.png',
    'images/bird-up.png'
]
MAX_VELOCITY = 6
class Bird(pygame.sprite.Sprite):
    def __init__(self, horizontal, vertical):

        super().__init__()
        self.image = pygame.image.load(birdimages[1])
        self.mask = pygame.mask.from_surface(self.image)

        self.x = horizontal
        self.y = vertical
        self.velocity = MAX_VELOCITY
        self.height = self.y
        self.flapped = False
        self.asleep = False
    
    def draw(self, window):  
        self.image = self.get_image()
        
        if self.asleep == True:
            self.image = pygame.transform.flip(self.image, False, True)
        
        elif self.velocity >= 6:
            self.image = pygame.transform.rotate(self.image, -25)
        else:
            self.image = pygame.transform.rotate(self.image, round(-3.5 * self.velocity, 1))
        window.blit(self.image, (self.x, self.y))
    
    def get_image(self):
        # Bird has had a collision and is 'asleep'
        if self.asleep == True:
            return pygame.image.load(birdimages[1])
        
        # Flapped wings
        if self.flapped == True:
            self.flapped = False
            return pygame.image.load(birdimages[0])
        # No flap but bird is climbing in altitude
        elif self.flapped == False and self.velocity < 0:
            return pygame.image.load(birdimages[0])
        # Wings raise ready to flap
        else:
            return pygame.image.load(birdimages[1])
            
    
    def flap(self):
        self.velocity = -13
        self.height = self.y
        self.flapped = True
    
    def move(self):
        self.y = self.y + self.velocity
        if self.velocity <= MAX_VELOCITY:
            self.velocity += 1.2
        else:
            self.velocity = MAX_VELOCITY

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def check_bounds(self, height):
        if self.y < 0 or self.y > height:
            return True
        
        return False
    
    def fall(self):
        if self.asleep == False:
            time.sleep(0.5)
            self.asleep = True
        self.y += 5