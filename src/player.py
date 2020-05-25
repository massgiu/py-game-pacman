import pygame
from src.settings import *

vec = pygame.math.Vector2
class Player:

    def __init__(self, app, starting_pos):
        self.app = app
        self.grid_pos = starting_pos #is a vec, so you can get x and y
        #This translate the coordinates of grid in pixel in order to be exactly inside a cell
        self.pix_pos = vec(self.grid_pos.x*self.app.cell_width+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                           self.grid_pos.y*self.app.cell_height+TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)
        print(self.grid_pos,self.pix_pos)

    def update(self):
        pass

    def draw(self):
        pygame.draw.circle(self.app.screen,PLAYER_COLOR,(int(self.pix_pos.x),int(self.pix_pos.y)),self.app.cell_width//2-2)
