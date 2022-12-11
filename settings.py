# game options/settings
TITLE = "Attack on ChoCho"
WIDTH = 500
HEIGHT = 750
FPS = 60
FONT_NAME = 'PixeloidSansBold-RpeJo.ttf'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
STAND = 'stand.png'
LEFT = 'left.png'
RIGHT = 'right.png'
JUMP = 'jump.png'
ENEMY = 'enemy.png'

# Player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -0.2
PLAYER_GRAV = 0.8
PLAYER_JUMP = 23

# Game properties
BOOST_POWER = 80
POW_SPAWN_PCT = 5
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
COIN_LAYER = 1
CLOUD_LAYER = 0

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
