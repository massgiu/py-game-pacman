from abc import ABC, abstractmethod
from pygame import Vector2 as vec
from src.settings import *


class AbstractCharacter(ABC):

    def __init__(self, app, init_grid_pos):
        self.app = app
        self.grid_pos = init_grid_pos  ##is a vec(col, row), so you can get x and y
        self.pix_pos = self.from_grid_to_pix_pos(self.grid_pos)
        self.direction = NEUTRAL
        self.image = None

    def update(self):
        pass

    def draw(self):
        pass

    def move(self):
        pass

    '''
    This fun translates the coordinates(row, col) of grid in pixel in order to be exactly inside a cell
    '''
    def from_grid_to_pix_pos(self, grid_pos):
        return vec(((grid_pos.x-1)%CELL_W)*CELL_W + TOP_BOTTOM_BUFFER+CELL_W //4,
                   ((grid_pos.y-1)%CELL_H)*CELL_H + TOP_BOTTOM_BUFFER+CELL_H //4)

    def from_pixel_to_grid_pos(self, pix_pos):
        col = (pix_pos[0] - TOP_BOTTOM_BUFFER + CELL_W // 2) // CELL_W + 1
        row = (pix_pos[1] - TOP_BOTTOM_BUFFER + CELL_H // 2) // CELL_H + 1
        return col, row

    def can_move(self, dir):
        return (self.grid_pos + dir) not in self.app.walls

    # def is_cell_centered(self):
    #     if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % CELL_W == 0:
    #         if self.direction == LEFT or self.direction == RIGHT or self.direction == NEUTRAL:
    #             return True
    #     if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % CELL_H == 0:
    #         if self.direction == UP or self.direction == DOWN or self.direction == NEUTRAL:
    #             return True
    #     return False

    def is_cell_centered(self):
        if (int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % CELL_W == 0 and
            int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % CELL_H == 0):
                return True
        return False
