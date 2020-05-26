import pygame
from src.settings import *

vec = pygame.math.Vector2
class Player:

    def __init__(self, app, starting_pos):
        self.app = app
        self.grid_pos = starting_pos #is a vec, so you can get x and y
        #This translate the coordinates of grid in pixel in order to be exactly inside a cell
        self.get_pix_pos()
        self.direction = RIGHT
        self.stored_direction = None
        self.able_to_move = True

    def update(self):
        if self.able_to_move: #this is True if is there is not a wall
            self.pix_pos+= self.direction #increases movement if there is not a wall
        if self.time_to_move(): #this is True if is in the grid
            if self.stored_direction !=None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        #Setting grid position from pixel pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER+self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER+self.app.cell_height//2) // self.app.cell_height+1

    def draw(self):
        pygame.draw.circle(self.app.screen,PLAYER_COLOR,(int(self.pix_pos.x),int(self.pix_pos.y)),self.app.cell_width//2-2)
        #Drawing rectangle in grid position
        pygame.draw.rect(self.app.screen, RED,
                         (int(self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2), int(self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2),
                         self.app.cell_width, self.app.cell_height),1)

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        self.pix_pos = vec(self.grid_pos.x * self.app.cell_width + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
            self.grid_pos.y * self.app.cell_height + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)
        print(self.grid_pos, self.pix_pos)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width ==0:
            if self.direction==LEFT or self.direction==RIGHT:
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height ==0:
            if self.direction==UP or self.direction==DOWN:
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        return True