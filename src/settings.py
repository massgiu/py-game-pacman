from pygame.math import Vector2 as vec
#Screen settings
WIDTH, HEIGHT = 610, 670
FPS = 60 # higher is factor, higher is speed animation
NUM_COLS = 28
NUM_ROWS = 30
TOP_BOTTOM_BUFFER = 50 #space around background to put text
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER
CELL_W = MAZE_WIDTH // NUM_COLS
CELL_H = MAZE_HEIGHT // NUM_ROWS
BACKGROUND_IMG_URL = '../media/maze.png'
#color settings
BLACK = (0, 0, 0)
OCHER = (170, 132, 58)
LIGHT_BLUE = (44, 167, 198)
WHITE = (255,255,255)
RED = (255,0,0)
GREY = (90,90,90)
YELLOW = (167, 179, 34)
COINS_COLOR = (230, 250, 0)
COINS_RADIUS = 5
BISCUITS_COLOR = (255, 0, 0)
BISCUITS_RADIUS = 7
ENEMY_COLORS = [(66,133,244),(219,68,55),(244,160,0),(15,157,88)]
ENEMY_PERSONALITIES = ['speedy', 'slow', 'random', 'scared']
#font settings
START_TEXT_SIZE = 16
START_FONT = 'arial_black'
#player settings
PLAYER_START_POS = None #row, col
PLAYER_COLOR = (190,194,15)
#direction
LEFT = vec(-1,0) #decreases 1 width pixel
RIGHT = vec(1,0) #increases 1 width pixel
UP = vec(0,-1) #decreases 1 height pixel
DOWN = vec(0,1) #increases 1 height pixel
NEUTRAL = vec(0,0)
PLAYER_SPEED = 4
ENEMY_SPEED = 1
TIME_TO_EAT = 10000
