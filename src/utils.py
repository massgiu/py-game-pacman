import pygame
from pygame import Vector2 as vec
from src.settings import *
from src.enemy import *

class Utils:

    def __init__(self):
        pass

    @classmethod
    def read_layout(self, background):
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
                        pygame.draw.rect(background, BLACK, (width * CELL_W, height * CELL_H,
                                                         CELL_W, CELL_H))
        return walls, coins, player_start_pos, enemies_start_pos

    @classmethod
    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        pos = list(pos)  # tuple are immutable, so list conversion
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, tuple(pos))

    @classmethod
    def draw_grid(self, background):
        # vertical lines
        for x in range(WIDTH // CELL_W):
            pygame.draw.line(background, GREY, (CELL_W * x, 0), (CELL_W * x, HEIGHT))
        # horizontal lines
        for y in range(WIDTH // CELL_H):
            pygame.draw.line(background, GREY, (0, CELL_H * y), (WIDTH, CELL_H * y))
        # draw lane
        # for coin in self.coins:
        #     pygame.draw.rect(self.background, YELLOW,
        #                      (coin[0]*self.cell_width, coin[1]*self.cell_height, self.cell_width, self.cell_height))

    @classmethod
    def draw_coins(self, screen, coins):
        for coin in coins:
            pygame.draw.circle(screen, COINS_COLOR, (int(coin.x * CELL_W + CELL_W // 2) + TOP_BOTTOM_BUFFER // 2,
                          int(coin.y * CELL_H + CELL_H // 2) + TOP_BOTTOM_BUFFER // 2),5)
    @classmethod
    def remove_life(self, player, player_start_pos, enemies, enemies_start_pos):
        player.lives -= 1
        if (player.lives == 0):
            return "game over"
        else:
            player.grid_pos = vec(player_start_pos)
            # form grid to pixel
            player.pix_pos = player.from_grid_to_pix_pos(player.grid_pos)
            player.direction = NEUTRAL
            #reposition for enemyes
            for index, enemy in enumerate(enemies):
                enemy.grid_pos = vec(enemies_start_pos[index])
                # form grid to pixel
                enemy.pix_pos = enemy.from_grid_to_pix_pos(enemy.grid_pos)
                enemy.direction = NEUTRAL
            return 'playing'

    @classmethod
    def reset(self, player, enemies, player_start_pos, enemies_start_pos, screen):
        player.lives = 3
        player.current_score = 0
        player.grid_pos = vec(player_start_pos)
        # form grid to pixel
        player.pix_pos = player.from_grid_to_pix_pos(player.grid_pos)
        player.direction = NEUTRAL
        for index, enemy in enumerate(enemies):
            enemy.grid_pos = vec(enemies_start_pos[index])
            # form grid to pixel
            enemy.pix_pos = enemy.from_grid_to_pix_pos(enemy.grid_pos)
            enemy.direction = NEUTRAL
        self.coins = []
        # redraws coins
        _, coins, _, _ = Utils.read_layout(screen)
        state = 'playing'
        return state, coins

    @classmethod
    def load_image(cls, name_img):
        image = pygame.image.load('../media/'+name_img+'.png')
        return pygame.transform.scale(image, (CELL_W, CELL_H))