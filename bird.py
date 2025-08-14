import pygame
import time

# Bird imgs w/ wings up / down for flapping animation
birdimages = [
    'images/bird-dn.png',
    'images/bird-up.png'
]

# Max speed bird can fall per frame
MAX_VELOCITY = 6

def blit_alpha(target, source, location, opacity):
    """ Cool trick to blit transparent image over pygame surface
        target -- background to be blit over
        source -- image to blit
        location -- x, y coordinates (tuple)
        opacity -- transparency (0 = transparent to 255 = opaque)
    """
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

class Bird(pygame.sprite.Sprite):
    """ Bird class

        Knows its position, its velocity, has a mask for collisions and 
        whether it is still flying or 'asleep'
        flapped -- tracks 
    """
    def __init__(self, horizontal, vertical): 
        """ Initiates pygame sprite and gives it a bird image
            horizontal -- starting x coord
            vertical -- starting y coord
        """
        super().__init__()
        self.image = pygame.image.load(birdimages[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.x = horizontal
        self.y = vertical
        self.velocity = MAX_VELOCITY
        self.height = self.y
        self.flapped = False
        self.asleep = False
        self.invulnerable = False

    def draw(self, window, invulnerable):
        """ Draws bird, taking into account current bird velocity and awake status

        """
        self.image = self.get_image()
        
        # Flips upside down if bird is asleep
        if self.asleep == True:
            self.image = pygame.transform.flip(self.image, False, True)
        
        # Tilt bird based on velocity
        elif self.velocity >= 6:
            self.image = pygame.transform.rotate(self.image, -25)
        else:
            self.image = pygame.transform.rotate(self.image, round(-3.5 * self.velocity, 1))
        if self.invulnerable:
            blit_alpha(window, self.image, (self.x, self.y), 128)
        else:
            window.blit(self.image, (self.x, self.y))
    
    def get_image(self):
        """ Returns bird image with wings up or down based on flap / awake status
        """
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
        """ Changes bird velocity after user presses space/up to flap
        """
        self.velocity = -13
        self.height = self.y
        self.flapped = True
    
    def move(self):
        """ Changes y coordinate and increases velocity up to a max falling velocity
            -ve velocity = climbing
            +ve velocity = falling
        """
        self.y = self.y + self.velocity
        if self.velocity <= MAX_VELOCITY:
            self.velocity += 1.2
        else:
            self.velocity = MAX_VELOCITY

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
    
    def check_bounds(self, height):
        """ Check that the bird is in bounds
        """
        if self.y < 0 or self.y > height:
            return True
        
        return False
    
    def fall(self):
        """ After collision, briefly pause then fall off screen
        """
        if self.asleep == False:
            time.sleep(0.5)
            self.asleep = True
        self.y += 5
    
    def check_powerup(self, powerup):
        offset = (self.x - powerup.x, self.y - powerup.y)
        if self.mask.overlap(powerup.mask, offset):
            print("got powerup!")
            return True
        
    def make_invulnerable(self):
        self.invulnerable = True
    
    def remove_invulnerable(self):
        self.invulnerable = False
        