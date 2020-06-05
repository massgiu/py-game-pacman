import pygame
from src.settings import *
from src.abstract_character import AbstractCharacter

vec = pygame.math.Vector2

class Player(AbstractCharacter):

    def __init__(self, app, init_grid_pos):
        super().__init__(app, init_grid_pos)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

    def update(self):
        if self.able_to_move: #this is True if is there is not a wall
            self.pix_pos+= self.direction * self.speed#increases movement if there is not a wall
        if self.time_to_move(): #this is True if is in the grid
            if self.stored_direction !=None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move(self.direction)
        #Setting grid position from pixel pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER+CELL_W//2)//CELL_W + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER+CELL_H//2) // CELL_H + 1
        if self.is_on_coin():
            self.eat_coin()

    def draw(self):
        pygame.draw.circle(self.app.screen,PLAYER_COLOR,(int(self.pix_pos.x),int(self.pix_pos.y)), CELL_W//2-2)
        #Drawing rectangle in grid position
        pygame.draw.rect(self.app.screen, RED,
                         (int(self.grid_pos[0]*CELL_W+TOP_BOTTOM_BUFFER//2), int(self.grid_pos[1]*CELL_H+TOP_BOTTOM_BUFFER//2),
                         CELL_W, CELL_H),1)
        #Drawig player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, ((2*CELL_W + CELL_W*x), HEIGHT-15), CELL_W//2)

    def is_on_coin(self):
        if self.grid_pos in self.app.coins:
            return self.time_to_move()
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score +=1

    def move(self, direction):
        self.stored_direction = direction

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % CELL_W ==0:
            if self.direction==LEFT or self.direction==RIGHT or self.direction==NEUTRAL:
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % CELL_H ==0 or self.direction==NEUTRAL:
            if self.direction==UP or self.direction==DOWN:
                return True
