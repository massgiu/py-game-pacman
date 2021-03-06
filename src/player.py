import pygame
from src.settings import *
from src.utils import Utils
from src.abstract_character import AbstractCharacter

vec = pygame.math.Vector2

class Player(AbstractCharacter):

    def __init__(self, app, init_grid_pos):
        super().__init__(app, init_grid_pos)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = PLAYER_SPEED
        self.power = False
        self.start_time = 0
        self.lives = 3

    def update(self):
        if self.able_to_move: #this is True if is there is not a wall
            self.pix_pos+= self.direction * self.speed #increases movement if there is not a wall
        if self.is_cell_centered(): #this is True if is centered in the grid
            if self.stored_direction !=None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move(self.direction) #True if in that 'direction' ther isn't a wall
        self.grid_pos[0], self.grid_pos[1] = self.from_pixel_to_grid_pos(self.pix_pos)
        self.eaten_coin()
        self.eaten_biscuit()

    def draw(self):
        if self.direction == RIGHT:
            self.image = 'right'
        elif self.direction == LEFT:
            self.image = 'left'
        elif self.direction == UP:
            self.image = 'up'
        else:
            self.image = 'down'
        # pygame.draw.circle(self.app.screen,PLAYER_COLOR,(int(self.pix_pos.x),int(self.pix_pos.y)), CELL_W//2-2)
        self.app.screen.blit(Utils.load_image(self.image),(int(self.pix_pos.x-CELL_W//2),int(self.pix_pos.y-CELL_H//2)))
        #Drawing rectangle in grid position
        # pygame.draw.rect(self.app.screen, RED,
        #                  (int(self.grid_pos[0]*CELL_W+TOP_BOTTOM_BUFFER//2), int(self.grid_pos[1]*CELL_H+TOP_BOTTOM_BUFFER//2),
        #                  CELL_W, CELL_H),1)
        #Drawig player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOR, ((2*CELL_W + CELL_W*x), HEIGHT-15), CELL_W//2)

    def eaten_coin(self):
        if self.grid_pos in self.app.coins and self.is_cell_centered():
            self.app.coins.remove(self.grid_pos)
            self.current_score += 1

    def eaten_biscuit(self):
        if self.grid_pos in self.app.biscuits and self.is_cell_centered():
            self.app.biscuits.remove(self.grid_pos)
            self.power = True
            self.start_time = pygame.time.get_ticks()

    # def eat_coin(self):
    #     self.app.coins.remove(self.grid_pos)
    #     self.current_score +=1

    def move(self, direction):
        self.stored_direction = direction