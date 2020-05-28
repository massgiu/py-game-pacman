from abc import ABC, abstractmethod
from pygame import Vector2 as vec
from src.settings import *

class AbstractCharacter(ABC):

    def __init__(self, app, init_grid_pos):
        self.app = app
        self.grid_pos = init_grid_pos #(row,col)
        self.pix_pos = self.get_pix_pos(self.grid_pos)
        self.direction = vec(1,0)

    def update(self):
        pass

    def draw(self):
        pass

    def move(self):
        pass

    def get_pix_pos(self, grid_pos):
        return vec(grid_pos.x * self.app.cell_width + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   grid_pos.y * self.app.cell_height + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def can_move(self,dir):
        return (self.grid_pos + dir) not in self.app.walls