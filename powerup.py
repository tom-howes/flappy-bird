import random
import pygame

powerup_images = [
    'images/slow.png'
]

class Powerup(pygame.sprite.Sprite):

    def __init__(self, pipes):
        """ Initiates a random powerup by picking one of the images from the array
            pipes -- array of pipes to be used to ensure powerup doesn't spawn on pipe
        """
        super().__init__()
        from flappy import WINDOW_HEIGHT
        from flappy import WINDOW_WIDTH

        # Pick a random powerup
        img_num = random.randint(0, len(powerup_images) - 1)

        self.image = pygame.image.load(powerup_images[img_num]).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        height = self.image.get_height()
        self.x = WINDOW_WIDTH
        self.y = random.randint(height + 30, WINDOW_HEIGHT - height - 30)
        self.up = True
        
        # Determines type of powerup
        self.type = powerup_images[img_num].removeprefix("images/").removesuffix(".png")

        # Avoid pipe collision
        for pipe in pipes: 
            while pipe.collision(self):
                self.y = random.randint(30, WINDOW_HEIGHT - 30)
    
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def move(self, velocity):
        """ Moves powerup icon
            velocity -- current velocity of the pipes
        """

        # Hover animation, gives icon the impression of the icon hovering up and down
        if self.x %  11 == 0:
            if self.up == True:
                self.y += 5
                self.up = False
            else:
                self.y -= 5
                self.up = True

        # Moves icon x coord at current speed of pipes
        self.x -= velocity
    
    def activate(self):
        """ Activates powerup and returns timer for powerup activation period
        """
        return 100, self.type