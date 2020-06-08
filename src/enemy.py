import pygame
import random

import src
from src.settings import *
from src.abstract_character import AbstractCharacter

vec = pygame.math.Vector2

class Enemy(AbstractCharacter):

    def __init__(self, app, init_grid_pos, index):
        super().__init__(app, init_grid_pos)
        self.radius = int(CELL_W // 2.3)
        self.personality = self.set_personality(index)
        self.target = self.set_target(self.personality)
        self.speed = self.set_speed()

    def update(self):
        self.target = self.set_target(self.personality)
        #to avoid to reach target pos (otherwise path=0)
        if self.target != self.grid_pos:
            # update pixel position
            self.pix_pos += self.direction * self.speed
        if self.is_cell_centered():
            self.move()
        # from pixel position find row and col
        self.grid_pos[0], self.grid_pos[1] = self.from_pixel_to_grid_pos(self.pix_pos)
        # self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + CELL_W // 2) // CELL_W + 1
        # self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + CELL_H // 2) // CELL_H + 1


    def set_target(self, personality):
        if personality == ENEMY_PERSONALITIES[0] or self.personality == ENEMY_PERSONALITIES[1]:  # speedy or slow
            return self.app.player.grid_pos  # target to pursuit
        else:  # scared mode
            if self.app.player.grid_pos[0] < NUM_COLS // 2 and self.app.player.grid_pos[1] < NUM_ROWS // 2:
                return vec(1, 1)  # top left
            elif self.app.player.grid_pos[0] > NUM_COLS // 2 and self.app.player.grid_pos[1] < NUM_ROWS // 2:
                return vec(NUM_COLS - 2, 1)  # top right
            elif self.app.player.grid_pos[0] < NUM_COLS // 2 and self.app.player.grid_pos[1] > NUM_ROWS // 2:
                return vec(1, NUM_ROWS - 1)  # down left
            else:
                return vec(NUM_COLS - 2, NUM_ROWS - 1)  # down right

    def set_speed(self):
        if (self.personality == ENEMY_PERSONALITIES[0] or  # speedy
                self.personality == ENEMY_PERSONALITIES[3]):  # scared
            return 2*ENEMY_SPEED
        else:
            return ENEMY_SPEED

    def draw(self, enemy_index, player_power):
        # pygame.draw.circle(self.app.screen, ENEMY_COLORS[enemy_index], (int(self.pix_pos.x), int(self.pix_pos.y)),
        #                    self.radius)
        if not player_power:
            if enemy_index == 0:
                self.image = 'blue'
            elif enemy_index == 1:
                self.image = 'green'
            elif enemy_index == 2:
                self.image = 'red'
            else:
                self.image = 'yellow'
            self.app.screen.blit(src.utils.Utils.load_image(self.image),
                                 (int(self.pix_pos.x - CELL_W // 2), int(self.pix_pos.y - CELL_H // 2)))
        else:
            self.image = 'dark'
            self.app.screen.blit(src.utils.Utils.load_image(self.image),
                                 (int(self.pix_pos.x - CELL_W // 2), int(self.pix_pos.y - CELL_H // 2)))


    def set_personality(self, index):
        return ENEMY_PERSONALITIES[index]

    def move(self):
        if self.personality == ENEMY_PERSONALITIES[2]: #random
            self.direction = self.get_random_direction()
        else:  # speedy, scared, slow
            self.direction = self.get_path_direction(self.target)

    '''
    This method creates random direction for enemy with 'random' personality
    '''
    def get_random_direction(self):
        while True:
            number = random.randint(0, 3)
            if number == 0:
                dir = DOWN  # increases row (down)
            elif number == 1:
                dir = RIGHT  # increases col (right)
            elif number == 2:
                dir = UP  # decreases row (up)
            else:
                dir = LEFT
            if self.can_move(dir):
                break  # right direction
        return dir

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(self.grid_pos, target)
        width_direc = next_cell[0] - self.grid_pos[0]
        height_direc = next_cell[1] - self.grid_pos[1]
        return vec(width_direc, height_direc)

    # starting_node = self.grid_pos
    # final_node = self.player.grid_pos
    def find_next_cell_in_path(self, starting_node, final_node):
        path = self.BFS(starting_node, final_node)
        if len(path) > 1:
            return path[1] #return only the first cell of the path (it's computed every cycle)

    def BFS(self, start, target):
        grid = [[0 for x in range(NUM_COLS)] for x in range(NUM_ROWS)]
        for cell in self.app.walls:
            if cell.x < NUM_COLS and cell.y < NUM_ROWS:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [RIGHT, LEFT, UP, DOWN]
                for neighbour in neighbours:
                    next_cell = current + neighbour
                    if 0 <= next_cell[0] < NUM_COLS:
                        if 0 <= next_cell[1] < NUM_ROWS:
                            if next_cell not in visited:
                                if grid[int(next_cell[1])][int(next_cell[0])] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest