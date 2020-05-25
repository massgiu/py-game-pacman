from pygame.math import Vector2 as vec
#Screen settings
WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_BUFFER = 50 #space around background to put text
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER
#color settings
BLACK = (0, 0, 0)
OCHER = (170, 132, 58)
LIGHT_BLUE = (44, 167, 198)
WHITE = (255,255,255)
RED = (255,0,0)
GREY = (90,90,90)
#font settings
START_TEXT_SIZE = 16
START_FONT = 'arial_black'
#player settings
PLAYER_START_POS = vec(1,8)
PLAYER_COLOR = (190,194,15)
