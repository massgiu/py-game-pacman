from pygame.math import Vector2 as vec
#Screen settings
WIDTH, HEIGHT = 610, 670
FPS = 60
NUM_COLS = 28
NUM_ROWS = 30
TOP_BOTTOM_BUFFER = 50 #space around background to put text
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER
#color settings
BLACK = (0, 0, 0)
OCHER = (170, 132, 58)
LIGHT_BLUE = (44, 167, 198)
WHITE = (255,255,255)
RED = (255,0,0)
GREY = (90,90,90)
YELLOW = (167, 179, 34)
#font settings
START_TEXT_SIZE = 16
START_FONT = 'arial_black'
#player settings
PLAYER_START_POS = vec(1,1) #row, col
PLAYER_COLOR = (190,194,15)
#direction
LEFT = vec(-1,0)
RIGHT = vec(1,0)
UP = vec(0,-1)
DOWN = vec(0,1)
