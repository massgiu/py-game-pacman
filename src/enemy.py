import pygame
import random
from src.settings import *
vec = pygame.math.Vector2

class Enemy:

    def __init__(self, app, init_grid_pos):
        self.app = app
        self.grid_pos = init_grid_pos #(row,col)
        self.pix_pos = self.get_pix_pos(self.grid_pos)
        self.radius = int(self.app.cell_width//2.3)
        self.direction = vec(1,0)
        self.personality = None

    def get_pix_pos(self, grid_pos):
        return vec(grid_pos.x * self.app.cell_width + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                           grid_pos.y * self.app.cell_height + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def update(self):
        #update pixel position
        self.pix_pos += self.direction
        if self.time_to_move():
            self.move()
        #from pixel position find row and col
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self, enemy_index):
        pygame.draw.circle(self.app.screen,  ENEMY_COLORS[enemy_index], (int(self.pix_pos.x), int(self.pix_pos.y)),self.radius)

    def set_personality(self, enemy_index):
        if self.personality == None:
            self.personality = ENEMY_PERSONALITIES[enemy_index]

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == LEFT or self.direction == RIGHT:
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == UP or self.direction == DOWN:
                return True
        return False

    def move(self):
        if self.personality==ENEMY_PERSONALITIES[2]:
            self.direction = self.get_random_direction()

    def get_random_direction(self):
        while True:
            number = random.randint(0, 3)
            if number == 0:
                dir = DOWN #increases row (down)
            elif number == 1:
                dir = RIGHT #increases col (right)
            elif number == 2:
                dir = UP #decreases row (up)
            else:
                dir = LEFT
            if self.can_move(dir):
                break #right direction
        return dir

    def can_move(self, dir):
        return (self.grid_pos + dir) not in self.app.walls