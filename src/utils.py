import pygame
from pygame import Vector2 as vec
from src.settings import *
class Utils:

    def __init__(self):
        pass

    @classmethod
    def read_layout(self, screen):
        walls = []
        coins = []
        enemies_start_pos = []
        with open('../media/wall.txt', 'r') as file:
            for height, line in enumerate(file):
                for width, char in enumerate(line):
                    if char == '1':
                        walls.append(vec(width, height))
                    elif char == 'C':
                        coins.append(vec(width, height))
                    elif char == 'P':
                        player_start_pos = [width, height]
                    elif char in ['2', '3', '4', '5']:
                        enemies_start_pos.append([width, height])
                    elif char == 'B':
                        pygame.draw.rect(screen, BLACK, (width * CELL_W, height * CELL_H,
                                                         CELL_W, CELL_H))
        return walls, coins, player_start_pos, enemies_start_pos
