import pygame, sys
from pygame import *

pygame.init()

# Constants 
WINDOWWIDTH = 500
WINDOWHEIGHT = 400
FPS = 30 

BLACK = (0,0,0)
WHITE = (255,255,255)

class Player(pygame.sprite.Sprite):
    '''This class represents the player'''
    def __init__(self, width, height):
        '''call the base (Sprite) constructor class'''
        super().__init__()

        # Create the player with width, height and color attributes
        self.image = pygame.Surface([width,height])
        self.image.fill(WHITE)

        # Draw the hero
        self.rect = self.image.get_rect()

        # Create player variables
        self.changex = 0
        self.changey = 0

    def move_left(self, move_x):
        '''move player left'''
        self.changex -= move_x

    def move_right(self, move_x):
        '''move player right'''
        self.changex += move_x

    def gravity(self):
        '''calculate gravity'''
        if self.changey == 0:
            self.changey = 0
        else:
            self.changey += .60

        if self.rect.bottom >= 360 and self.changey >= 0:
            self.changey = 0
            self.rect.y = 330
        
    def jump(self):
        '''make player jump'''
        if self.rect.bottom == 360:
            self.changey = -10

    def update(self):
        '''gravity'''
        self.gravity()
        
        '''update player movement'''
        self.rect.x += self.changex
        self.rect.y += self.changey

        '''boundary checking'''
        if self.rect.x < 0:
            self.rect.x = 0

        if self.rect.x > WINDOWWIDTH - self.rect.width:
            self.rect.x = WINDOWWIDTH - self.rect.width

# FPS to control screen updates
FPSCLOCK = pygame.time.Clock()

# create display surface
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Classic Arcade')

# List that contains all sprites in the game
active_sprites_list = pygame.sprite.Group()
        
# Spawn sprite and set x, y location
player = Player(30, 30)
player.rect.x = WINDOWWIDTH / 2 - player.rect.centerx
player.rect.y = 330

# Add the sprites to the list of objects
active_sprites_list.add(player)

while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left(5)
            if event.key == pygame.K_RIGHT:
                player.move_right(5)
            if event.key == pygame.K_UP:
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.move_left(-5)
            if event.key == pygame.K_RIGHT:
                player.move_right(-5)

    # Game logic goes here
    active_sprites_list.update()

    # Drawing code goes here
    DISPLAYSURF.fill(BLACK)
        
    # Draw sprites at once all/refresh the position of the player
    active_sprites_list.draw(DISPLAYSURF)

    pygame.display.update() # update screen
    FPSCLOCK.tick(FPS) # limit frames per second
