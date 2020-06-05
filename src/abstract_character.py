from abc import ABC, abstractmethod
from pygame import Vector2 as vec
from src.settings import *

class AbstractCharacter(ABC):

    def __init__(self, app, init_grid_pos):
        self.app = app
        self.grid_pos = init_grid_pos ##is a vec(col, row), so you can get x and y
        self.pix_pos = self.get_pix_pos(self.grid_pos)
        self.direction = NEUTRAL

    def update(self):
        pass

    def draw(self):
        pass

    def move(self):
        pass


    '''
    This fun translates the coordinates of grid in pixel in order to be exactly inside a cell
    '''
    def get_pix_pos(self, grid_pos):
        return vec(grid_pos.x * CELL_W + TOP_BOTTOM_BUFFER // 2 + CELL_W // 2,
                   grid_pos.y * CELL_H + TOP_BOTTOM_BUFFER // 2 + CELL_H // 2)

    def can_move(self,dir):
        return (self.grid_pos + dir) not in self.app.walls