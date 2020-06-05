import pygame
import random
from src.settings import *

vec = pygame.math.Vector2


class Enemy:

    def __init__(self, app, init_grid_pos, index):
        self.app = app
        self.grid_pos = init_grid_pos  # (row,col)
        self.pix_pos = self.get_pix_pos(self.grid_pos)
        self.radius = int(self.app.cell_width // 2.3)
        self.direction = vec(0,0)
        self.personality = self.set_personality(index)
        self.target = self.set_target(self.personality)
        self.speed = self.set_speed()

    def get_pix_pos(self, grid_pos):
        return vec(grid_pos.x * self.app.cell_width + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   grid_pos.y * self.app.cell_height + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def update(self):
        self.target = self.set_target(self.personality)
        #to avoid to reach target pos (otherwise path=0)
        if self.target != self.grid_pos:
            # update pixel position
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            self.move(self.target)
        # from pixel position find row and col
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2) // self.app.cell_height + 1

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
            return 2
        else:
            return 1

    def draw(self, enemy_index):
        pygame.draw.circle(self.app.screen, ENEMY_COLORS[enemy_index], (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.radius)

    def set_personality(self, index):
        return ENEMY_PERSONALITIES[index]

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == LEFT or self.direction == RIGHT or self.direction==NEUTRAL:
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == UP or self.direction == DOWN or self.direction==NEUTRAL:
                return True
        return False

    def move(self, target):
        if self.personality == ENEMY_PERSONALITIES[2]: #random
            self.direction = self.get_random_direction()
        else:  # speedy, scared, slow
            self.direction = self.get_path_direction(target)

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

    def can_move(self, dir):
        return (self.grid_pos + dir) not in self.app.walls

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
