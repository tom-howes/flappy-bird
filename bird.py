import pygame

birdimages = [
    'images/bird-dn.png',
    'images/bird-up.png'
]
MAX_VELOCITY = 6
class Bird(pygame.sprite.Sprite):
    def __init__(self, horizontal, vertical):

        super().__init__()
        self.image = pygame.image.load(birdimages[1])
        self.wings = 'up'
        self.mask = pygame.mask.from_surface(self.image)

        self.x = horizontal
        self.y = vertical
        self.velocity = MAX_VELOCITY
        self.height = self.y
        self.flapped = False
    
    def draw(self, window):  
        self.image = self.get_image()
        # - 3.5
        
        if self.velocity >= 6:
            self.image = pygame.transform.rotate(self.image, -25)
        else:
            self.image = pygame.transform.rotate(self.image, round(-3.5 * self.velocity, 1))
        # # - 3.5
        # elif 0 < self.velocity < 6:
        #     self.image = pygame.transform.rotate(self.image, -10)
        # elif self.velocity < -6:
        #     self.image = pygame.transform.rotate(self.image, 20)
        print("speed: ", self.velocity)
        window.blit(self.image, (self.x, self.y))
    
    def get_image(self):
        if self.flapped == True:
            self.flapped = False
            return pygame.image.load(birdimages[0])
        elif self.flapped == False and self.velocity < 0:
            return pygame.image.load(birdimages[0])
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